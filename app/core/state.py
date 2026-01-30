"""
Conversation State Module
Pydantic models for tracking trip planning state.
"""
from pydantic import BaseModel
from typing import Optional, List


class TripDetails(BaseModel):
    """Model to store trip planning details"""
    destination: Optional[str] = None
    origin: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    travelers: int = 1
    interests: List[str] = []


class ConversationState(BaseModel):
    """Model to track the current conversation state"""
    session_id: str
    trip: TripDetails = TripDetails()
    messages_count: int = 0
