# app/state.py

from typing import TypedDict, List, Optional


class TravelState(TypedDict):
    messages: List[str]

    destination: Optional[str]
    city_code: Optional[str]

    start_date: Optional[str]
    end_date: Optional[str]

    rain_expected: Optional[bool]
    rain_approved: Optional[bool]

    budget: Optional[int]

    flights: Optional[list]
    hotels: Optional[list]
