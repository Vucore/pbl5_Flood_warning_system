from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from app.services import sensor_service
import asyncio
from app.services import data_processing
from app.database.SensorData import SensorData
from app.services import handl_data_global
router = APIRouter()

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
            await asyncio.sleep(20)  # Gửi ping mỗi 20 giây
            await websocket.send_text("ping")
    except Exception as e:
        print(f"Heartbeat error: {e}")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Tạo task cho heartbeat
    heartbeat_task = asyncio.create_task(keep_connection_alive(websocket))
    
    try:
        while True:
            try:
                message = await websocket.receive_text()
                if message == "ping":
                    continue  # Bỏ qua tin nhắn ping
                    
                print(f"Received: {message}")
                
                parts = message.split(";")
                temperature = float(parts[0].strip())
                air_pressure = float(parts[1].strip())
                air_humidity = float(parts[2].strip())
                rainfall = float(parts[3].strip())
                soil_humidity = float(parts[4].strip())
                water_level = float(parts[5].strip())


                sensor_data = SensorData(timestamp=None, rainfall = rainfall, soil_humidity = soil_humidity, air_humidity = air_humidity, air_pressure= air_pressure, temperature = temperature, water_level = water_level)

                sensor_data_process = data_processing.clean_and_validate_data(sensor_data)

                if(sensor_data_process):
                    # Lưu vào database
                    # sensor_service.process_sensor_data(sensor_data=sensor_data)
                    # Luu vao bien global
                    handl_data_global.save_global_data(sensor_data_process)
                    # print(handl_data_global.get_current_data().body.decode("utf-8"))
                else:
                    print("dữ liệu bị lỗi nên bỏ qua")
                # Gửi dữ liệu cho tất cả clients
                await manager.broadcast(sensor_data_process)
                
            except (ValueError, IndexError) as e:
                print(f"Invalid data format: {e}")
                continue
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        await manager.disconnect(websocket)
    finally:
        heartbeat_task.cancel()  # Hủy task heartbeat khi kết thúc