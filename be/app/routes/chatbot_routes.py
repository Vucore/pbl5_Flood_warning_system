from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from ..services import chatbot_services
import logging

router = APIRouter()
# Logging setup
logging.basicConfig(level=logging.INFO)

class ChatRequest(BaseModel):
    message: str
    rag: bool
    language: Optional[str] = None


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_message = request.message
        is_RAG = request.rag

        if not user_message:
            return "Please provide a message."
        if is_RAG:
            response = chatbot_services.process_bot_response_RAG(user_message)
            return response
        else:
            response = chatbot_services.process_bot_response(user_message)
            return response
        # Debug log response
        # logging.info(f"User message: {user_message}, Bot response: {response}")
        # return JSONResponse(content={"response": response, "language": language})
    
    except Exception as e:
        logging.error(f"Server error: {e}")
        # return JSONResponse(content={"response": "An error occurred on the server.", "error": str(e)}, status_code=500)
        return "An error occurred on the server."
