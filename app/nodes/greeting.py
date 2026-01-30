# app/nodes/greeting.py

from app.state import TravelState


def greeting_node(state: TravelState) -> TravelState:
    return {
        **state,
        "messages": state["messages"]
        + [
            "Hey! 🌍 I’m your travel buddy.\n"
            "Tell me where you want to travel and your dates "
            "(for example: *Paris from 12th to 18th March*)."
        ],
    }
