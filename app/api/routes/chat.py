from fastapi import APIRouter
from pydantic import BaseModel
from app.core.agent import ChatAgent

router = APIRouter()

# Request model
class ChatRequest(BaseModel):
    user_input: str

# Response model
class ChatResponse(BaseModel):
    response: str

# Initialize the agent
agent = ChatAgent()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    answer = agent.run(request.user_input)
    return ChatResponse(response=answer)
