# app/llm.py

import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """
    Returns a configured Groq LLM instance.
    """
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=1024,
    )
