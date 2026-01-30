"""
Chat Agent Module
LangChain agent with travel-focused tools.
"""
import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from app.core.llm import get_llm
from app.core.memory import get_memory
from app.tools.weather import get_weather
from app.tools.itenary import create_itinerary
from app.tools.flight_search import search_flights
from app.tools.budget import calculate_budget
from app.tools.trip_info import get_trip_info

# Load environment variables
load_dotenv()


class ChatAgent:
    """
    Travel Assistant Agent powered by LangChain.
    Helps users plan trips, check weather, find flights, and more.
    """
    
    def __init__(self):
        self.llm = get_llm()
        self.memory = get_memory()
        
        # Define all available tools
        self.tools = [
            Tool(
                name="Weather",
                func=get_weather,
                description="Get current weather for a city. Input: city name (e.g., 'Paris', 'Tokyo')"
            ),
            Tool(
                name="Itinerary",
                func=create_itinerary,
                description="Create a travel itinerary. Input: destination and days (e.g., '3 day Paris itinerary')"
            ),
            Tool(
                name="FlightSearch",
                func=search_flights,
                description="Search for flights. Input: route (e.g., 'Delhi to Paris', 'flights from Mumbai to London')"
            ),
            Tool(
                name="Budget",
                func=calculate_budget,
                description="Calculate trip budget. Input: destination and days (e.g., 'budget for Tokyo 5 days')"
            ),
            Tool(
                name="TripInfo",
                func=get_trip_info,
                description="Get destination information. Input: city name (e.g., 'Paris', 'Bali')"
            )
        ]
        
        # System message for the agent
        system_message = """You are SathChalo, a friendly and helpful travel assistant. 
        
Your job is to help users plan amazing trips! You can:
- Check weather conditions for any city
- Create day-by-day itineraries
- Search for flights between cities
- Estimate trip budgets
- Provide destination information and travel tips

Be conversational, enthusiastic about travel, and always provide helpful suggestions.
When users ask about a destination, proactively offer relevant information like weather, budget estimates, or top attractions.

Always use the tools available to you to provide accurate, up-to-date information."""

        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            agent_kwargs={
                "system_message": system_message
            },
            handle_parsing_errors=True
        )
    
    def run(self, user_input: str) -> str:
        """
        Process user input and return agent response.
        
        Args:
            user_input: The user's message
            
        Returns:
            Agent's response string
        """
        try:
            response = self.agent.run(user_input)
            return response
        except Exception as e:
            return f"I apologize, I encountered an error: {str(e)}. Please try rephrasing your question."
