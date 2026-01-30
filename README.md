# 🌍 SathChalo - Your AI Travel Buddy

An AI-powered travel assistant chatbot built with LangChain, Groq LLM, FastAPI, and Streamlit.

## ✨ Features

- 🌤️ **Weather Information** - Real-time weather data via Open-Meteo API
- ✈️ **Flight Search** - Search for flights between cities
- 📅 **Trip Itineraries** - Get day-by-day travel plans
- 💰 **Budget Estimates** - Calculate trip costs
- 📍 **Destination Info** - Learn about popular destinations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

The `.env` file should contain your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the API Server

```bash
uvicorn app.api.main:app --reload
```

API will be available at: http://127.0.0.1:8000

### 4. Start the Streamlit UI

In a new terminal:

```bash
streamlit run app/ui/streamlit_app.py
```

UI will open at: http://localhost:8501

## 📁 Project Structure

```
sathchalo/
├── app/
│   ├── api/              # FastAPI backend
│   │   ├── main.py       # API entry point
│   │   └── routes/
│   │       └── chat.py   # Chat endpoint
│   │
│   ├── core/             # LangChain core
│   │   ├── agent.py      # Chat agent with tools
│   │   ├── llm.py        # Groq LLM setup
│   │   ├── memory.py     # Conversation memory
│   │   └── state.py      # State models
│   │
│   ├── tools/            # LangChain tools
│   │   ├── weather.py    # Open-Meteo weather
│   │   ├── flight_search.py
│   │   ├── budget.py
│   │   ├── trip_info.py
│   │   └── itenary.py
│   │
│   ├── services/         # Business logic
│   │   ├── travel_service.py
│   │   └── planner.py
│   │
│   └── ui/
│       └── streamlit_app.py
│
├── .env                  # API keys (not in git)
├── requirements.txt
└── README.md
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |
| `/chat/` | POST | Chat with assistant |

### Chat API Example

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What is the weather in Paris?"}'
```

## 💡 Example Questions

- "What's the weather like in Tokyo?"
- "Plan a 5-day trip to Bali"
- "Search flights from Delhi to Dubai"
- "Budget estimate for Paris for 3 days"
- "Tell me about Goa"

## 🛠️ Tech Stack

- **LLM**: Groq (Llama 3.3 70B)
- **Framework**: LangChain
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Weather API**: Open-Meteo (free)

## 📝 License

MIT License
