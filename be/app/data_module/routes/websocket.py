# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# import asyncio
# from ..Utils import data_processing
# from ..services import sensor_services
# from ..database.SensorData import SensorData
# from ..Utils.global_state import GlobalState
# router = APIRouter()

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#         print("Client connected via WebSocket")

#     async def disconnect(self, websocket: WebSocket):
#         if websocket in self.active_connections:
#             self.active_connections.remove(websocket)
#             print("Client disconnected")

#     async def broadcast(self, message: SensorData):
#         message_json = data_processing.convert_to_json(message)
#         if message_json is None:
#             return
#         for connection in self.active_connections:
#             try:
#                 await connection.send_text(message_json)
#             except:
#                 await self.disconnect(connection)

# manager = ConnectionManager()


# async def keep_connection_alive(websocket: WebSocket):
#     try:     
#         while True:
#             await asyncio.sleep(20)  # Gửi ping mỗi 20 giây
#             await websocket.send_text("ping")
#     except Exception as e:
#         print(f"Heartbeat error: {e}")

    
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)

#     # Tạo task cho heartbeat
#     heartbeat_task = asyncio.create_task(keep_connection_alive(websocket))
    
#     try:
#         while True:
#             try:
#                 message = await websocket.receive_text()
#                 if message == "ping":
#                     continue
                 
#                 print(f"Server received data: {message}")
                
#                 sensor_data = data_processing.convert_message_to_sensor_data(message=message)
#                 # Lưu vào database
#                 # save_task = asyncio.create_task(
#                 #     sensor_services.save_sensor_data_to_db(sensor_data=sensor_data)
#                 # )
#                 sensor_data_standardize = data_processing.clean_and_validate_data(sensor_data)
                
#                 if(sensor_data_standardize):
#                     # Luu vao bien global
#                     GlobalState.save_global_data_sensor(sensor_data_standardize)
#                 else:
#                     print("Dữ liệu bị lỗi nên bỏ qua")
#                 # Gửi dữ liệu cho tất cả clients
#                 await manager.broadcast(sensor_data_standardize)
#                 # await save_task
                
#             except (ValueError, IndexError) as e:
#                 print(f"Invalid data format: {e}")
#                 continue
                
#     except WebSocketDisconnect:
#         await manager.disconnect(websocket)
#     except Exception as e:
#         print(f"Error: {e}")
#         await manager.disconnect(websocket)
#     finally:
#         heartbeat_task.cancel()  # Hủy task heartbeat khi kết thúc



















from fastapi import APIRouter, WebSocket, WebSocketDisconnect, FastAPI
import firebase_admin
import asyncio
from ..Utils import data_processing
from ..services import sensor_services
from ..database.SensorData import SensorData
from ..Utils.global_state import GlobalState
from firebase_admin import credentials
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

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
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        db_url = os.getenv("FIREBASE_DB")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })
        print("✅ Firebase initialized")

    yield

    print("🛑 App shutdown")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Gọi khi app khởi động
#     if not firebase_admin._apps:
#         cred = credentials.Certificate("pbl5-microbit-firebase-adminsdk-fbsvc-e304393036.json")
#         firebase_admin.initialize_app(cred, {
#             'databaseURL': 'https://pbl5-microbit-default-rtdb.firebaseio.com/'
#         })
#         print("✅ Firebase initialized")

#     yield  

#     # Gọi khi app shutdown (nếu cần)
#     print("🛑 App shutdown")

router = APIRouter(lifespan=lifespan)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    heartbeat_task = asyncio.create_task(keep_connection_alive(websocket))

    fetch_task = None
    try:
        async def fetch_and_broadcast_from_firebase():
            # last_timestamp = None
            while True:
                sensor_data = await sensor_services.get_latest_sensor_data_from_firebase()
                # print(f"[Firebase Data] Received: {sensor_data.__dict__ if sensor_data else None}")
                if not sensor_data:
                    await asyncio.sleep(5)
                    continue

                # if sensor_data.timestamp != last_timestamp:
                #     last_timestamp = sensor_data.timestamp

                sensor_data_standardized = data_processing.clean_and_validate_data(sensor_data)
                # print(f"[Data Processing] Standardized: {sensor_data_standardized.__dict__ if sensor_data_standardized else None}")
                if sensor_data_standardized:
                    GlobalState.save_global_data_sensor(sensor_data_standardized)
                    await manager.broadcast(sensor_data_standardized)
                else:
                    print("Dữ liệu Firebase không hợp lệ")
                await asyncio.sleep(5)

        fetch_task = asyncio.create_task(fetch_and_broadcast_from_firebase())

        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                continue  # giữ kết nối sống

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await manager.disconnect(websocket)
    finally:
        heartbeat_task.cancel()
        if fetch_task:
            fetch_task.cancel()
