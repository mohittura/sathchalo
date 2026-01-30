# app/memory.py

from typing import Dict
from app.state import TravelState

MEMORY_STORE: Dict[str, TravelState] = {}


def load_state(session_id: str) -> TravelState | None:
    return MEMORY_STORE.get(session_id)


def save_state(session_id: str, state: TravelState):
    MEMORY_STORE[session_id] = state
