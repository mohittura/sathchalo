"""
FastAPI Main Application
Entry point for the SathChalo API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes import chat

# Load environment variables at startup
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="SathChalo API",
    description="Travel Buddy API - Your AI-powered travel assistant",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])


@app.get("/", tags=["Health"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to SathChalo API! 🌍",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sathchalo-api"
    }
