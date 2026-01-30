from langchain_core.messages import AIMessage
from app.tools import check_weather

def weather_check_node(state):
    # 🛑 HARD STOP if required fields missing
    if not state.get("destination"):
        return state

    if not state.get("start_date") or not state.get("end_date"):
        return state

    # Optional: future range guard
    if not state.get("forecast_available", True):
        return state

    weather = check_weather(
        city=state["destination"],
        start_date=state["start_date"],
        end_date=state["end_date"],
    )

    state["rain_expected"] = weather["rain_expected"]
    state["weather"] = weather
    return state
