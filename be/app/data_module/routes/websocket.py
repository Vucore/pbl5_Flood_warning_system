from fastapi import APIRouter, WebSocket, WebSocketDisconnect, FastAPI, HTTPException
import firebase_admin
from pydantic import BaseModel
import asyncio
from ..Utils import data_processing
from ..services import firebase_services
from ..database.SensorData import SensorData
from ..Utils.global_state import GlobalState
from firebase_admin import credentials, db
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from ...config import get_settings

settings = get_settings()
load_dotenv()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Client connected via WebSocket")

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print("Client disconnected")

    async def broadcast(self, message: SensorData):
        message_json = data_processing.convert_to_json(message)
        if message_json is None:
            return
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except:
                await self.disconnect(connection)

manager = ConnectionManager()


async def keep_connection_alive(websocket: WebSocket):
    try:
        while True:
            await asyncio.sleep(20)
            await websocket.send_text("ping")
    except Exception as e:
        print(f"Heartbeat error: {e}")
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firebase_credentials_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.FIREBASE_DB
        })
        print("✅ Firebase initialized")

    yield

    print("🛑 App shutdown")

router = APIRouter(lifespan=lifespan)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    heartbeat_task = asyncio.create_task(keep_connection_alive(websocket))

    fetch_task = None
    try:
        async def fetch_and_broadcast_from_firebase():
            while True:
                sensor_data = await firebase_services.get_latest_sensor_data_from_firebase()
                if not sensor_data:
                    await asyncio.sleep(5)
                    continue

                sensor_data_standardized = data_processing.clean_and_validate_data(sensor_data)

                if sensor_data_standardized:
                    GlobalState.save_global_data_sensor(sensor_data_standardized)
                    await manager.broadcast(sensor_data_standardized)
                else:
                    print("Dữ liệu bị lỗi nên bỏ qua")
                await asyncio.sleep(10)

        fetch_task = asyncio.create_task(fetch_and_broadcast_from_firebase())
        await fetch_task

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        await manager.disconnect(websocket)
    finally:
        if fetch_task:
            fetch_task.cancel()
        # heartbeat_task.cancel()