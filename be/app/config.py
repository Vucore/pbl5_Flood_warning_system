from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Cấu hình cơ bản
    APP_NAME: str = "Flood Warning System"
    DEBUG: bool = False
    
    # Cấu hình CORS
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Cấu hình WebSocket
    WS_PING_INTERVAL: int = 20
    WS_PING_TIMEOUT: int = 20

    # Cấu hình Email
    GMAIL_USER: str
    GMAIL_PASS: str

    # Cấu hình Model
    ENCODER_MODEL_NAME: str
    FLOOD_MODEL_PATH: str

    # Cấu hình Firebase
    FIREBASE_DB: str
    FIREBASE_CREDENTIALS_PATH: str = "pbl5-microbit-firebase-adminsdk-fbsvc-e304393036.json"
    
    @property
    def firebase_credentials_path(self) -> str:
        """Get the absolute path to Firebase credentials file"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), self.FIREBASE_CREDENTIALS_PATH)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()