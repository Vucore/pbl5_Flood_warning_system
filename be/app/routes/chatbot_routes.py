from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import json
from services import chatbot_service
from services import handl_data_global

router = APIRouter()

# Logging setup
logging.basicConfig(level=logging.INFO)

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = None


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_message = request.message
        language = request.language

        if not user_message:
            return JSONResponse(content={"response": "Please provide a message.", "language": language}, status_code=400)

        latest_data = json.loads(handl_data_global.get_current_data().body.decode("utf-8"))
        
        response = chatbot_service.process_message(
            user_message,
            language,
            latest_data,
            "normal"
        )

        # Debug log response
        logging.info(f"User message: {user_message}, Bot response: {response}, laster: {latest_data}")
        return JSONResponse(content={"response": response, "language": language})
    
    except Exception as e:
        logging.error(f"Server error: {e}")
        return JSONResponse(content={"response": "An error occurred on the server.", "error": str(e)}, status_code=500)
