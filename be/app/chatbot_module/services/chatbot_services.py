from ..base.init import ChatbotBase
# from ..base.Utils.utils import preprocess_text
chatbot = ChatbotBase()

def process_bot_response(message: str):
    response = chatbot.generate_response_noRAG(message)
    return response

def process_bot_response_RAG(message: str):
    response = chatbot.generate_response_RAG(message)
    return response
