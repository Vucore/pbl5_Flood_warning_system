from fastapi import FastAPI
from app.routes.chatbot_routes import router as chatbot_router  # Đảm bảo import router
from app.routes import websocket
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định frontend của bạn như ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router đúng cách
app.include_router(chatbot_router, prefix="/api")
app.include_router(websocket.router)