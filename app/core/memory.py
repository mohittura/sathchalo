"""
Conversation Memory Module
Simple memory implementation for maintaining chat history.
"""
from langchain.memory import ConversationBufferMemory


def get_memory():
    """
    Returns a ConversationBufferMemory for the LangChain agent.
    Stores the conversation history in memory.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    return memory
