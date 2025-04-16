from fastapi import FastAPI
from .routes import websocket
from fastapi.middleware.cors import CORSMiddleware

websoc = FastAPI()

websoc.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định frontend của bạn như ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router đúng cách
# app.include_router(chatbot_routes.router, prefix="/api")
websoc.include_router(websocket.router)