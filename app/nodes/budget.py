# app/nodes/budget.py

from app.state import TravelState


def budget_node(state: TravelState) -> TravelState:
    return {
        **state,
        "messages": state["messages"]
        + [
            "Awesome 👍 Let’s continue.\n"
            "What’s your budget per night for accommodation?"
        ],
    }
