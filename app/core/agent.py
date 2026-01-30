from app.core.llm import get_llm
from app.core.memory import get_memory
from langchain.agents import initialize_agent, Tool
from app.tools.weather import get_weather
from app.tools.itenary import create_itenary

class ChatAgent:
    def __init__(self):
        self.llm = get_llm()
        self.memory = get_memory()

        # Define tools
        self.tools = [
            Tool(
                name="Weather",
                func=get_weather,
                description="Get the weather for a city"
            ),
            Tool(
                name="Itenary",
                func=create_itenary,
                description="Generate a travel itinerary"
            )
        ]

        # Initialize LangChain agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )

    def run(self, user_input: str) -> str:
        return self.agent.run(user_input)
