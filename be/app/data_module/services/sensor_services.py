from ..database.SensorData import SensorData
from firebase_admin import db
from ..database.SensorData import SensorData

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