# app/tools/amadeus.py

import os
import time
import requests
from typing import Dict, List
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

AMADEUS_BASE_URL = "https://test.api.amadeus.com"

_token_cache = {
    "access_token": None,
    "expires_at": 0,
}


def _get_access_token() -> str:
    """
    Fetch or reuse Amadeus OAuth token.
    """
    global _token_cache

    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Amadeus credentials not configured")

    response = requests.post(
        f"{AMADEUS_BASE_URL}/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=10,
    )
    response.raise_for_status()
    token_data = response.json()

    _token_cache = {
        "access_token": token_data["access_token"],
        "expires_at": time.time() + token_data["expires_in"] - 60,
    }

    return _token_cache["access_token"]


@tool
def search_hotels(
    city_code: str,
    budget: int,
    check_in: str,
    check_out: str,
) -> dict:
    """
    Search hotels using Amadeus API based on budget.

    Args:
        city_code (str): IATA city code (e.g. PAR, NYC)
        budget (int): Max price per night
        check_in (str): YYYY-MM-DD
        check_out (str): YYYY-MM-DD

    Returns:
        Dict with hotel recommendations
    """

    token = _get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "cityCode": city_code,
        "checkInDate": check_in,
        "checkOutDate": check_out,
        "priceRange": f"0-{budget}",
        "radius": 5,
        "radiusUnit": "KM",
        "ratings": "3,4,5",
    }

    response = requests.get(
        f"{AMADEUS_BASE_URL}/v2/shopping/hotel-offers",
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()
    data = response.json()

    hotels: List[Dict] = []
    for offer in data.get("data", [])[:5]:
        hotel = offer.get("hotel", {})
        hotels.append(
            {
                "name": hotel.get("name"),
                "rating": hotel.get("rating"),
                "address": hotel.get("address", {}).get("lines", []),
            }
        )

    return {
        "total_found": len(hotels),
        "hotels": hotels,
    }

@tool
def resolve_city_code(city: str) -> str:
    """
    Resolve city name to IATA city code.
    """

    token = _get_access_token()

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "keyword": city,
        "subType": "CITY",
    }

    response = requests.get(
        f"{AMADEUS_BASE_URL}/v1/reference-data/locations",
        headers=headers,
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json().get("data", [])
    if not data:
        raise ValueError("City code not found")

    return data[0]["iataCode"]

@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
) -> list:
    """
    Search flight offers between two cities using Amadeus API.

    Args:
        origin (str): Origin IATA airport or city code (e.g. DEL)
        destination (str): Destination IATA airport or city code (e.g. CDG)
        departure_date (str): Departure date in YYYY-MM-DD format

    Returns:
        list: A list of flight offer objects (limited set).
    """
    token = _get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
    }

    response = requests.get(
        f"{AMADEUS_BASE_URL}/v2/shopping/flight-offers",
        headers=headers,
        params=params,
        timeout=15,
    )
    response.raise_for_status()

    data = response.json().get("data", [])
    return data[:3]

