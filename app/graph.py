# app/graph.py

from langgraph.graph import StateGraph, END
from app.state import TravelState

# Nodes
from app.nodes import (
    greeting_node,
    trip_info_node,
    weather_check_node,
    rain_interrupt_node,
    budget_node,
)

# Tools
from app.tools import search_hotels


# -------------------------
# Helper Nodes
# -------------------------

def rain_approval_node(state: TravelState) -> TravelState:
    """
    Parses user response to rain warning.
    """
    user_reply = state["messages"][-1].lower()

    approved = user_reply in ["yes", "y", "sure", "continue", "ok"]

    return {
        **state,
        "rain_approved": approved,
        "messages": state["messages"]
        + [
            "Got it 👍 Continuing with planning."
            if approved
            else "Understood. Trip planning stopped due to weather concerns."
        ],
    }


def capture_budget_node(state: TravelState) -> TravelState:
    """
    Parses user budget input.
    """
    user_reply = state["messages"][-1]

    try:
        budget = int("".join(filter(str.isdigit, user_reply)))
    except ValueError:
        budget = None

    return {
        **state,
        "budget": budget,
        "messages": state["messages"]
        + [f"Great! Looking for stays within ₹{budget} per night."],
    }


def hotel_search_node(state: TravelState) -> TravelState:
    """
    Calls Amadeus hotel search tool.
    """
    # NOTE: city_code should ideally come from a geocoding step
    city_code = state["destination"][:3].upper()

    result = search_hotels.invoke(
        {
            "city_code": city_code,
            "budget": state["budget"],
            "check_in": state["start_date"],
            "check_out": state["end_date"],
        }
    )

    if result["total_found"] == 0:
        message = "😕 No hotels found within your budget."
    else:
        hotels = "\n".join(
            [
                f"- {h['name']} ⭐ {h.get('rating', 'N/A')}"
                for h in result["hotels"]
            ]
        )
        message = f"🏨 Here are some great hotel options:\n{hotels}"

    return {
        **state,
        "messages": state["messages"] + [message],
    }


# -------------------------
# Routing Logic
# -------------------------

def route_after_weather(state: TravelState) -> str:
    """
    If rain expected → ask for approval.
    Otherwise → go directly to budget.
    """
    if state["rain_expected"]:
        return "rain_interrupt"
    return "budget"


def route_after_rain_approval(state: TravelState) -> str:
    """
    If user approves → continue.
    Else → end conversation.
    """
    if state["rain_approved"]:
        return "budget"
    return END

def should_check_weather(state):
    return (
        state.get("destination")
        and state.get("start_date")
        and state.get("end_date")
    )

# -------------------------
# Graph Definition
# -------------------------

def build_graph():
    builder = StateGraph(TravelState)

    # Core nodes
    builder.add_node("greeting", greeting_node)
    builder.add_node("trip_info", trip_info_node)
    builder.add_node("weather", weather_check_node)
    builder.add_node("rain_interrupt", rain_interrupt_node)
    builder.add_node("rain_approval", rain_approval_node)
    builder.add_node("budget_prompt", budget_node)
    builder.add_node("capture_budget", capture_budget_node)
    builder.add_node("hotel_search", hotel_search_node)

    # Entry
    builder.set_entry_point("greeting")

    # Flow
    builder.add_edge("greeting", "trip_info")
    builder.add_conditional_edges("trip_info", should_check_weather,{True:"weather",False:END})

    builder.add_conditional_edges(
        "weather",
        route_after_weather,
        {
            "rain_interrupt": "rain_interrupt",
            "budget": "budget_prompt",
        },
    )

    builder.add_edge("rain_interrupt", "rain_approval")

    builder.add_conditional_edges(
        "rain_approval",
        route_after_rain_approval,
        {
            "budget": "budget_prompt",
            END: END,
        },
    )

    builder.add_edge("budget_prompt", "capture_budget")
    builder.add_edge("capture_budget", "hotel_search")
    builder.add_edge("hotel_search", END)

    return builder.compile()


graph = build_graph()
