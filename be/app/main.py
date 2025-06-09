from fastapi import FastAPI
from .chatbot_module.routes import chatbot_routes
from .data_module.routes import websocket, func_routes
from .floodrisk_module.routes import flood_risk_routes
# from .sensor_module.sensor_controller import router as sensor_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from .config import get_settings
import os
import mimetypes

# Thêm MIME type cho JavaScript
mimetypes.add_type("application/javascript", ".js")

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Mount static files với cấu hình MIME type
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")

# Route cho trang chủ
@app.get("/")
async def read_root():
    return FileResponse("app/static/html/login.html")

# Route riêng cho file JavaScript
# @app.get("/static/js/{filename}")
# async def get_js_file(filename: str):
#     file_path = os.path.join("app/static/js", filename)
#     if os.path.exists(file_path):
#         with open(file_path, "rb") as f:
#             content = f.read()
#         return Response(content=content, media_type="application/javascript")
#     return Response(status_code=404)

# Đăng ký router đúng cách
app.include_router(chatbot_routes.router, prefix="/api")
app.include_router(func_routes.router, prefix="/api")
app.include_router(flood_risk_routes.router, prefix="/api")
app.include_router(websocket.router)
# app.include_router(sensor_router, prefix="/api")