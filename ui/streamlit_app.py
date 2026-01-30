# ui/streamlit_app.py

import uuid
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Travel Buddy 🌍", page_icon="🌍")

st.title("🌍 Travel Buddy")
st.caption("Your AI-powered travel planning companion")

# -----------------------------
# Session handling
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Where do you want to travel?")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    # Send to backend
    response = requests.post(
        API_URL,
        json={
            "session_id": st.session_state.session_id,
            "message": user_input,
        },
        timeout=60,
    )

    if response.status_code != 200:
        st.error("Backend error:")
        st.code(response.text)
        st.stop()

    data = response.json()

    # The backend returns full message list
    assistant_messages = data["messages"][len(st.session_state.messages) - 1 :]

    for msg in assistant_messages:
        st.session_state.messages.append(
            {"role": "assistant", "content": msg}
        )
        st.chat_message("assistant").write(msg)
