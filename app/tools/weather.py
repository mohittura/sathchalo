import requests
from typing import Dict
from langchain.tools import tool
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd


# -----------------------------
# Open-Meteo client setup
# -----------------------------

cache_session = requests_cache.CachedSession(
    ".openmeteo_cache", expire_after=3600
)
retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


# -----------------------------
# Helper: city → lat/lon
# -----------------------------

def _geocode_city(city: str) -> Dict:
    """
    Resolve a city name to latitude and longitude using Open-Meteo geocoding.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    results = response.json().get("results")
    if not results:
        raise ValueError(f"Could not find location for city: {city}")

    return {
        "latitude": results[0]["latitude"],
        "longitude": results[0]["longitude"],
        "name": results[0]["name"],
        "country": results[0].get("country"),
    }


# -----------------------------
# LangChain Tool
# -----------------------------

from datetime import date, timedelta

@tool
def check_weather(
    city: str,
    start_date: str,
    end_date: str,
) -> Dict:
    """
    Check if rain is expected for a city between given dates using Open-Meteo.
    """

    # -----------------------------
    # Forecast window guard
    # -----------------------------
    today = date.today()
    max_forecast_date = today + timedelta(days=16)

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    # ❗ Forecast not available yet
    if start > max_forecast_date:
        return {
            "city": city,
            "forecast_available": False,
            "rain_expected": None,
            "message": (
                "Weather forecasts are not available this far in advance. "
                "I can still help plan your trip if you'd like."
            ),
        }

    # Clamp end date to forecast horizon
    if end > max_forecast_date:
        end = max_forecast_date

    # -----------------------------
    # Normal Open-Meteo flow
    # -----------------------------
    location = _geocode_city(city)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": ["precipitation_sum"],
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()
    precipitation = daily.Variables(0).ValuesAsNumpy()

    df = pd.DataFrame({
        "date": pd.date_range(start=start, end=end),
        "precipitation_mm": precipitation,
    })

    rain_days = df[df["precipitation_mm"] > 0.1]

    return {
        "city": location["name"],
        "country": location["country"],
        "forecast_available": True,
        "rain_expected": not rain_days.empty,
        "rain_days": rain_days.to_dict(orient="records"),
        "total_rain_mm": float(df["precipitation_mm"].sum()),
    }