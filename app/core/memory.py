# from langgraph.store.memory import ConversationBufferMemory
# from langgraph.schema import messages_from_dict, messages_to_dict
# from langchain.memory.chat_message_histories import InMemoryChatMessageHistory

# def get_memory():
#     """
#     Returns a ConversationBufferMemory compatible with LangChain agents
#     and ChatGroq. Uses InMemoryChatMessageHistory to store messages.
#     """
#     memory_saver = InMemoryChatMessageHistory()
    
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",   # key used internally by agent
#         input_key="input",           # key for user input
#         chat_memory=memory_saver,    # Use InMemoryChatMessageHistory
#         return_messages=True         # return BaseMessage objects
#     )
#     return memory
