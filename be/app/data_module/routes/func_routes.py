from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
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
        result = func_services.update_user_status_sqlite(email=email, isOnline=isOnline, lastLogin=lastLogin)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.get("/user/list")
async def get_list_user():
    try:
        result = func_services.get_list_user()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AdminAuthRequest(BaseModel):
    password: str

@router.post("/admin/auth")
async def admin_auth(request: AdminAuthRequest):
    try:
        password = request.password
        result = func_services.admin_auth(password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class PasswordRequest(BaseModel):
    password: str

@router.post("/admin/password")
def set_password(request: PasswordRequest):
    try:
        password = request.password
        func_services.update_pass_admin(password)
        return {"message": "Password saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class WaterLevelRequest(BaseModel):
    threshold_cm: int

@router.post("/sensor/water-level")
def set_water_level(request: WaterLevelRequest):
    try:
        threshold = request.threshold_cm
        result = firebase_services.update_distance_sensor_in_firebase(threshold)
        return {"message": "Threshold saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history", response_class=PlainTextResponse)
async def get_chat_history():
    try:
        return func_services.get_chat_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))