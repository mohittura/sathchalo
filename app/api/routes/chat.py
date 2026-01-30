"""
Chat API Routes
Endpoints for chatting with the travel assistant.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.agent import ChatAgent

router = APIRouter()


# Request model
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    user_input: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_input": "What's the weather like in Paris?"
            }
        }


# Response model
class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    success: bool = True


# Initialize the agent (singleton)
agent = ChatAgent()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat with the travel assistant.
    
    Send a message and get a helpful response about travel planning,
    weather, flights, budgets, and more!
    """
    if not request.user_input.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        answer = agent.run(request.user_input)
        return ChatResponse(response=answer, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
