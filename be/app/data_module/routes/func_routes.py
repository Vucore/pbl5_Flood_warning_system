from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
import logging
from ..services import func_services

router = APIRouter()
# Logging setup
logging.basicConfig(level=logging.INFO)

class RegisterRequest(BaseModel):
    username: str
    email: str
    phone: str
    address: Optional[str] = None


@router.post("/register")
async def regis_endpoint(request: RegisterRequest):
    try:
        username = request.username
        email = request.email
        phone = request.phone
        address = request.address

        response = func_services.handle_User_Signup(username, email, phone, address)
        return response
    
    except Exception as e:
        logging.error(f"Server error: {e}")
        return "An error occurred on the server."
