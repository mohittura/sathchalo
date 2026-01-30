"""
SathChalo - Clean ChatGPT-style UI
"""
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat/"

st.set_page_config(
    page_title="SathChalo",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Exact ChatGPT styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    #MainMenu, footer, header, .stDeployButton {display: none !important;}
    
    .stApp {
        background-color: #212121;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 1px solid #2f2f2f;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 1rem;
    }
    
    /* Sidebar text */
    .sidebar-item {
        color: #ececec;
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .sidebar-item:hover {
        background: #2f2f2f;
    }
    
    /* Main content */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Header */
    .header-text {
        color: #10a37f;
        font-size: 1rem;
        font-weight: 500;
        padding: 1rem 2rem;
    }
    
    /* Center content */
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
    }
    
    .main-title {
        color: #ececec;
        font-size: 2rem;
        font-weight: 500;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        max-width: 48rem;
        margin: 0 auto;
        padding: 1.5rem 0;
    }
    
    [data-testid="stChatMessage"] p {
        color: #ececec !important;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Chat input */
    .stChatInput {
        max-width: 48rem;
        margin: 0 auto 2rem auto;
    }
    
    .stChatInput > div {
        background: #2f2f2f !important;
        border: 1px solid #424242 !important;
        border-radius: 24px !important;
    }
    
    .stChatInput input {
        background: transparent !important;
        color: #ececec !important;
    }
    
    .stChatInput input::placeholder {
        color: #8e8e8e !important;
    }
    
    /* Hide streamlit button styling */
    .stButton > button {
        background: transparent;
        border: none;
        color: #ececec;
        text-align: left;
        padding: 0.5rem 0.75rem;
        width: 100%;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: #2f2f2f;
    }
    
    /* Username at bottom */
    .username {
        position: fixed;
        bottom: 1rem;
        left: 1rem;
        color: #10a37f;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if st.button("➕ New chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('<div class="sidebar-item">🔍 Search chats</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🖼️ Images</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📱 Apps</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🤖 Tools</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="username">Mohit Manglani</div>', unsafe_allow_html=True)

# Header
st.markdown('<div class="header-text">SathChalo 1.0</div>', unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome or messages
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="center-content">
        <div class="main-title">What can I help with?</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                resp = requests.post(API_URL, json={"user_input": prompt}, timeout=60)
                answer = resp.json().get("response", "Error") if resp.status_code == 200 else "Error"
            except:
                answer = "Cannot connect to API server."
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
