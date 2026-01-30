# app/nodes/rain_interrupt.py

from app.state import TravelState


def rain_interrupt_node(state: TravelState) -> TravelState:
    """
    Human-in-the-loop interrupt when rain is expected.
    """

    return {
        **state,
        "messages": state["messages"]
        + [
            f"⚠️ There are chances of rain in {state['destination']} "
            f"between {state['start_date']} and {state['end_date']}.\n"
            "Do you want to continue planning? (yes / no)"
        ],
    }
