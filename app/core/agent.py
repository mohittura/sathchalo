"""
Chat Agent Module
Simple travel assistant using LangChain and Groq LLM.
"""
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq

from app.tools.weather import get_weather
from app.tools.itenary import create_itinerary
from app.tools.flight_search import search_flights
from app.tools.budget import calculate_budget
from app.tools.trip_info import get_trip_info

# Load environment variables
load_dotenv()

# System prompt for the travel assistant
SYSTEM_PROMPT = """You are SathChalo, a friendly and helpful travel assistant.

Your job is to help users plan amazing trips! When users ask about travel, you should:
1. Understand their query
2. Use the appropriate tool to get information
3. Provide a helpful, conversational response

Available tools and when to use them:
- WEATHER: When user asks about weather/climate in a city (call: get_weather)
- ITINERARY: When user wants a travel plan for a destination (call: create_itinerary)
- FLIGHTS: When user asks about flights between cities (call: search_flights)
- BUDGET: When user asks about trip costs/budget (call: calculate_budget)
- TRIPINFO: When user asks about a destination's info (call: get_trip_info)

Be enthusiastic about travel! Use emojis appropriately. Provide helpful tips.
If you're unsure which tool to use, ask clarifying questions.

IMPORTANT: When responding, if you detect a tool should be used, I will call it for you.
Just provide a natural, helpful response based on the context."""


class ChatAgent:
    """
    Travel Assistant using simple LLM with tool integration.
    """
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        self.chat_history = []
        
        # Tool mapping
        self.tools = {
            "weather": get_weather,
            "itinerary": create_itinerary,
            "flights": search_flights,
            "budget": calculate_budget,
            "tripinfo": get_trip_info
        }
    
    def _detect_and_call_tool(self, user_input: str) -> str:
        """
        Detect which tool to use based on user input and call it.
        Returns tool result or empty string if no tool needed.
        """
        input_lower = user_input.lower()
        
        # Weather detection
        if any(word in input_lower for word in ["weather", "temperature", "climate", "hot", "cold", "rain"]):
            # Extract city - simple approach
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ["in", "for", "at"]:
                    if i + 1 < len(words):
                        city = " ".join(words[i+1:]).strip("?.!")
                        return self.tools["weather"](city)
            # If no city found, try the last word
            city = words[-1].strip("?.!") if words else "Paris"
            return self.tools["weather"](city)
        
        # Itinerary detection
        if any(word in input_lower for word in ["itinerary", "plan", "trip", "days", "day"]):
            return self.tools["itinerary"](user_input)
        
        # Flight detection
        if any(word in input_lower for word in ["flight", "fly", "flights", "airline"]):
            return self.tools["flights"](user_input)
        
        # Budget detection
        if any(word in input_lower for word in ["budget", "cost", "expense", "price", "afford", "money"]):
            return self.tools["budget"](user_input)
        
        # Trip info detection
        if any(word in input_lower for word in ["tell me about", "info", "information", "about", "destination", "visit"]):
            # Extract destination
            for phrase in ["tell me about", "about", "info on", "information about"]:
                if phrase in input_lower:
                    dest = input_lower.split(phrase)[-1].strip().strip("?.!")
                    return self.tools["tripinfo"](dest)
            return self.tools["tripinfo"](user_input)
        
        return ""
    
    def run(self, user_input: str) -> str:
        """
        Process user input and return response.
        """
        try:
            # Try to detect and call a tool
            tool_result = self._detect_and_call_tool(user_input)
            
            # Build messages
            messages = [SystemMessage(content=SYSTEM_PROMPT)]
            
            # Add chat history (last 6 messages)
            for msg in self.chat_history[-6:]:
                messages.append(msg)
            
            # Add current user message
            if tool_result:
                # Include tool result in the context
                enhanced_input = f"User asked: {user_input}\n\nTool result:\n{tool_result}\n\nPlease provide a helpful response based on this information."
                messages.append(HumanMessage(content=enhanced_input))
            else:
                messages.append(HumanMessage(content=user_input))
            
            # Get LLM response
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Update chat history
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=answer))
            
            return answer
            
        except Exception as e:
            return f"I apologize, I encountered an error: {str(e)}. Please try again!"
