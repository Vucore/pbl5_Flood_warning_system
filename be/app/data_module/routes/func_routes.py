from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from ..services import func_services, firebase_services

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

        response = await func_services.handle_user_signup(username, email, phone, address)
        return response
    
    except Exception as e:
        logging.error(f"Server error: {e}")
        return "An error occurred on the server."

class LoginRequest(BaseModel):
    email: str

@router.post("/login")
async def login_endpoint(request: LoginRequest):
    try:
        email = request.email
        response = func_services.handle_login(email)
        return response
    except Exception as e:
        logging.error(f"Server error: {e}")
        return "An error occurred on the server."    

class SensorToggleRequest(BaseModel):
    sensorId: str
    isTurned: bool

@router.post("/sensor/toggle")
async def toggle_sensor(request: SensorToggleRequest):
    try:
        # Add your logic here to handle the sensor state
        # For example, update a database or trigger some action
        print(f"Toggling sensor {request.sensorId} to {request.isTurned}")
        sensor_name = request.sensorId
        state = request.isTurned
        result = firebase_services.update_state_sensor_in_firebase(sensor_name, state)
        
        return {"status": result, "message": f"Sensor {request.sensorId} state updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensor/status")
async def get_sensor_status():
    try:
        result = firebase_services.get_sensor_status()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class UserStatus(BaseModel):
    email: str
    isGuest: bool
    isOnline: bool
    lastLogin: int

@router.post("/user/login-state")
async def save_user_state(status: UserStatus):
    try:
        email = status.email
        isGuest = status.isGuest
        isOnline = status.isOnline
        lastLogin = status.lastLogin
        result = firebase_services.update_user_status(email, isGuest, isOnline, lastLogin)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    