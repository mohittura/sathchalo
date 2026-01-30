"""
Weather Tool
Fetches real weather data using Open-Meteo API (free, no API key needed).
"""
import requests


def get_weather(location: str) -> str:
    """
    Get current weather for a location using Open-Meteo API.
    
    Args:
        location: City name (e.g., "Paris", "Tokyo")
    
    Returns:
        Weather description string
    """
    try:
        # Step 1: Get coordinates from city name using geocoding API
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(
            geocode_url,
            params={"name": location, "count": 1},
            timeout=10
        )
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"Could not find location: {location}"
        
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]
        country = geo_data["results"][0].get("country", "")
        
        # Step 2: Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(
            weather_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "temperature_unit": "celsius"
            },
            timeout=10
        )
        weather_data = weather_response.json()
        
        current = weather_data.get("current_weather", {})
        temp = current.get("temperature", "N/A")
        wind_speed = current.get("windspeed", "N/A")
        
        # Weather code interpretation
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy", 
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm"
        }
        
        weather_code = current.get("weathercode", 0)
        weather_desc = weather_codes.get(weather_code, "Unknown")
        
        return (
            f"Weather in {city_name}, {country}:\n"
            f"- Temperature: {temp}°C\n"
            f"- Conditions: {weather_desc}\n"
            f"- Wind Speed: {wind_speed} km/h"
        )
        
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
