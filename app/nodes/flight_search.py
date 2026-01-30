# app/nodes/flight_search.py

from app.state import TravelState
from app.tools import search_flights


def flight_search_node(state: TravelState) -> TravelState:
    flights = search_flights.invoke(
        {
            "origin": "DEL",  # later: detect user origin
            "destination": state["city_code"],
            "departure_date": state["start_date"],
        }
    )

    return {
        **state,
        "flights": flights,
        "messages": state["messages"]
        + [f"✈️ Found {len(flights)} flight options."],
    }
