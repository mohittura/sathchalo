"""
SathChalo - Travel Buddy Streamlit App
A friendly chat interface for travel planning.
"""
import streamlit as st
import requests

# Configuration
API_URL = "http://127.0.0.1:8000/chat/"

# Page config
st.set_page_config(
    page_title="SathChalo - Travel Buddy",
    page_icon="✈️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .main-header {
        text-align: center;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>✈️ SathChalo</h1>
    <p>Your AI Travel Buddy - Plan your perfect trip!</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Namaste! I'm SathChalo, your travel buddy!\n\nI can help you with:\n- 🌤️ Weather information\n- ✈️ Flight searches\n- 📅 Trip itineraries\n- 💰 Budget estimates\n- 📍 Destination info\n\nWhere would you like to go?"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your travel plans..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={"user_input": prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "I couldn't process that request.")
                else:
                    answer = f"⚠️ API Error (Status: {response.status_code}). Make sure the API server is running!"
                    
            except requests.exceptions.ConnectionError:
                answer = "⚠️ Cannot connect to the API server.\n\nPlease make sure to start the API first:\n```\nuvicorn app.api.main:app --reload\n```"
            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"
        
        st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar with quick actions
with st.sidebar:
    st.header("🚀 Quick Actions")
    
    if st.button("🌤️ Check Weather"):
        st.session_state.quick_action = "What's the weather like in Paris?"
        
    if st.button("📅 Plan a Trip"):
        st.session_state.quick_action = "Plan a 3-day trip to Tokyo"
        
    if st.button("💰 Estimate Budget"):
        st.session_state.quick_action = "Budget estimate for Bali 5 days"
        
    if st.button("✈️ Search Flights"):
        st.session_state.quick_action = "Flights from Delhi to Dubai"
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Made with ❤️ by SathChalo Team")
