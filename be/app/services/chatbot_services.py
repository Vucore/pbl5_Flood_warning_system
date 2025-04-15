from ..ai.ChatBot.init_chatbot import ChatbotBase

chatbot = ChatbotBase()

def process_bot_response(message: str):
    response = chatbot.generate_response(message)
    return response
