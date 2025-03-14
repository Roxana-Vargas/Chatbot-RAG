# from langchain.memory import ConversationBufferMemory

# class ChatMemory:
#     def __init__(self):
#         self.memory = ConversationBufferMemory()

#     def add_message(self, user_message, bot_response):
#         """Stores the conversation history."""
#         self.memory.save_context({"input": user_message}, {"output": bot_response})

#     def get_memory(self):
#         """Retrieves the conversation history."""
#         return self.memory.load_memory_variables({})["history"]
