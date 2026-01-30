# app/main.py
from app.memory import load_state, save_state
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.graph import graph
from app.state import TravelState
import json

app = FastAPI()

from fastapi import HTTPException
from langchain_core.messages import HumanMessage
import traceback

@app.post("/chat")
def chat(payload: dict):
    try:
        session_id = payload.get("session_id", "default")

        state = load_state(session_id) or {
            "messages": ["hello"],
            "destination": None,
            "city_code": None,
            "start_date": None,
            "end_date": None,
            "rain_expected": None,
            "rain_approved": None,
            "budget": None,
            "flights": None,
            "hotels": None,
        }

        # ✅ FIX 1: wrap user message correctly
        state["messages"].append(
            HumanMessage(content=payload["message"])
        )

        result = graph.invoke(state)

        save_state(session_id, result)

        # ✅ FIX 2: return ONLY the assistant’s latest message
        last_message = result["messages"][-1]

        return {
            "response": last_message.content
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
