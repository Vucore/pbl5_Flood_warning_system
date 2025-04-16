from fastapi import FastAPI
from .routes import chatbot_routes
from fastapi.middleware.cors import CORSMiddleware
chatbot = FastAPI()

chatbot.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định frontend của bạn như ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router đúng cách
chatbot.include_router(chatbot_routes.router, prefix="/api")
