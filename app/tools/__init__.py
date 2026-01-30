"""
Tool registry for the Travel Buddy agent.

Only tools imported here are considered public and safe
to be used by LangGraph nodes or LLM agents.

This makes tool discovery explicit, auditable, and scalable.
"""

# Weather tools
from app.tools.weather import check_weather

# Amadeus travel tools
from app.tools.amadeus import search_hotels

__all__ = [
    # Weather
    "check_weather",

    # Hotels
    "search_hotels",
]
