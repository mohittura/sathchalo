# app/nodes/city_code.py

from app.state import TravelState
from app.tools import resolve_city_code


def city_code_node(state: TravelState) -> TravelState:
    code = resolve_city_code.invoke({"city": state["destination"]})

    return {
        **state,
        "city_code": code,
        "messages": state["messages"]
        + [f"📍 Resolved city code: {code}"],
    }
