import asyncio
import websockets
import random

async def simulate_esp8266():
    uri = "ws://localhost:8000/ws"   # Địa chỉ WebSocket server của bạn

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        try:
            while True:
                # Tạo dữ liệu giả lập
                temperature = random.uniform(0.0, 100.0)
                air_pressure = random.uniform(1000.0, 1020.0)
                air_humidity = random.uniform(30.0, 70.0)
                rainfall = random.uniform(0.0, 1024.0)
                soil_humidity = random.uniform(0.0, 1024.0)
                water_level = random.uniform(0.0, 50.0)

                # Định dạng dữ liệu thành chuỗi
                data = f"{temperature};{air_pressure};{air_humidity};{rainfall};{soil_humidity};{water_level}"
                await websocket.send(data)
                print(f"Sent: {data}")

                # Đợi 2 giây trước khi gửi dữ liệu tiếp theo
                await asyncio.sleep(5)

        except Exception as e:
            print(f"Error: {e}")

# Chạy hàm simulate_esp8266
asyncio.get_event_loop().run_until_complete(simulate_esp8266())