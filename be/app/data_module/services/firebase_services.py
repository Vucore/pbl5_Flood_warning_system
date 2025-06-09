from ..database.SensorData import SensorData
from firebase_admin import db
from ..database.SensorData import SensorData
from fastapi import HTTPException
import time

async def get_latest_sensor_data_from_firebase() -> SensorData | None:
    ref = db.reference("sensor_data")
    data = ref.order_by_key().limit_to_last(1).get()

    if not data:
        return None

    latest_data = list(data.values())[0]

    try:
        return SensorData(
            temperature=latest_data.get("temperature"),
            air_pressure=latest_data.get("air_pressure"),
            air_humidity=latest_data.get("air_humidity"),
            rainfall=latest_data.get("rainfall"),
            soil_humidity=latest_data.get("soil_humidity"),
            water_level=latest_data.get("water_level"),
        )
    except Exception as e:
        print(f"[Firebase Parse Error] {e}")
        return None

def update_state_sensor_in_firebase(sensor_name: str, state: bool):
    try:
        # Lấy reference đến Firebase
        ref = db.reference('/control_state')
        
        # Kiểm tra sensor name hợp lệ
        valid_sensors = ['rain', 'soil_humd', 'temp', 'water_level', 'air_humd', 'air_pres']
        if sensor_name not in valid_sensors:
            raise ValueError(f"Tên sensor không hợp lệ. Chọn một trong: {valid_sensors}")
            
        # Cập nhật chỉ một sensor và timestamp
        ref.update({
            sensor_name: state,
            'timestamp': int(time.time())
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi cập nhật sensor: {str(e)}")

    return "success"

def get_sensor_status():
    try:
        ref = db.reference('/control_state')
        data = ref.get()
        
        if not data:
            return []

        # Chuyển đổi dữ liệu thành dạng list các sensor
        sensor_list = []
        for sensor_id, is_turned in data.items():
            if sensor_id == "timestamp":
                continue
            sensor_list.append({
                "sensorId": sensor_id,
                "isTurned": is_turned
            })
        return sensor_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy trạng thái sensor: {str(e)}")


def update_user_status(email : str, isGuest: bool, isOnline: bool, lastLogin: int):
    try:
        user_id = email.split("@")[0]
        ref = db.reference(f'/users/{user_id}')
        
        # Cập nhật dữ liệu
        ref.update({
            "email": email,
            "isGuest": isGuest,
            "isOnline": isOnline,
            "lastLogin": lastLogin
        })

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# def send_control(control: ControlState):
#     try:
#         # Lấy reference đến Firebase Realtime Database
#         ref = db.reference(control_data_path)
        
#         # Gửi dữ liệu lên Firebase
#         ref.set({
#             'rain_sensor': control.rain_sensor,
#             'soil_humd': control.soil_humd,
#             'bme280': control.bme280,
#             'sieu_am': control.sieu_am,
#             'timestamp': int(time.time()),
#         })

    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error sending data to Firebase: {str(e)}")









# async def get_latest_sensor_data_from_firebase() -> SensorData | None:
#     ref = db.reference("sensor_data")
#     data = ref.order_by_key().limit_to_last(1).get()
#     # print(f"[Firebase raw data] {data}")

#     if not data:
#         return None

#     # Lấy phần tử mới nhất từ dict
#     latest_data = list(data.values())[0]

#     try:
#         # Chuyển timestamp thành định dạng datetime string
#         timestamp = latest_data.get("timestamp")
#         if timestamp:
#             # Chuyển timestamp thành datetime object
#             dt = datetime.fromtimestamp(timestamp)
#             # Format lại thành string theo định dạng mong muốn
#             formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             formatted_time = None

#         return SensorData(
#             temperature=latest_data.get("temperature"),
#             air_pressure=latest_data.get("air_pressure"),
#             air_humidity=latest_data.get("air_humidity"),
#             rainfall=latest_data.get("rainfall"),
#             soil_humidity=latest_data.get("soil_humidity"),
#             water_level=latest_data.get("water_level"),
#             timestamp=formatted_time  # Sử dụng timestamp đã được format
#         )
#     except Exception as e:
#         print(f"[Firebase Parse Error] {e}")
#         return None