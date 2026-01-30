from fastapi import FastAPI
from app.api.routes import chat

app = FastAPI(title="SATHCHALO API")

# Include routes
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to SATHCHALO API"}
