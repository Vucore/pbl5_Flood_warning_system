from ..base.init import ChatbotBase

chatbot = ChatbotBase()

def process_bot_response(message: str):
    response = chatbot.generate_response(message)
    return response

def process_bot_response_RAG(message: str):
    response = chatbot.generate_response_RAG(message)
    return response
