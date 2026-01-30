# app/nodes/trip_info.py

from typing import Optional
from pydantic import BaseModel, Field
from app.state import TravelState
from app.llm import get_llm

llm = get_llm()


class TripInfo(BaseModel):
    destination: str = Field(description="City name")
    start_date: str = Field(description="YYYY-MM-DD")
    end_date: str = Field(description="YYYY-MM-DD")


def trip_info_node(state: TravelState) -> TravelState:
    user_message = state["messages"][-1]

    extractor = llm.with_structured_output(TripInfo)
    trip = extractor.invoke(user_message)

    return {
        **state,
        "destination": trip.destination,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "messages": state["messages"]
        + [
            f"✈️ Trip detected: {trip.destination} "
            f"from {trip.start_date} to {trip.end_date}"
        ],
    }
