from langchain_groq import ChatGroq
import os

def get_llm():
    # Make sure you have GROQ_API_KEY in your .env
    api_key = os.getenv("GROQ_API_KEY")

    return ChatGroq(
        api_key=api_key,
        temperature=0,
        model="llama-3.3-70b-versatile"
    )
