from app.database.SensorData import SensorData
from datetime import datetime
from fastapi.responses import JSONResponse

MAX_HISTORY_SIZE = 288
sensor_data_history = []
current_warning_level = "normal"  # "normal", "watch", "warning", "severe"
current_language = "vi"
translations = {
    "en": {
        "temperature": "Temperature",
        "air_pressure": "Air Pressure",
        "air_humidity": "Air Humidity",
        "rainfall": "Rainfall",
        "soil_humidity": "Soil Humidity",
        "water_level": "Water Level",
        "normal": "Normal",
        "watch": "Watch",
        "warning": "Warning",
        "severe": "Severe",
        "flood_warning": "Flood Warning",
        "normal_message": "All parameters are within normal ranges.",
        "watch_message": "Some parameters indicate potential risk. Monitor the situation.",
        "warning_message": "Warning! Flood risk is elevated. Be prepared.",
        "severe_message": "Severe warning! High flood risk. Take immediate action."
    },
    "vi": {
        "temperature": "Nhiệt độ",
        "air_pressure": "Áp suất không khí",
        "air_humidity": "Độ ẩm không khí",
        "rainfall": "Lượng mưa",
        "soil_humidity": "Độ ẩm đất",
        "water_level": "Mực nước",
        "normal": "Bình thường",
        "watch": "Theo dõi",
        "warning": "Cảnh báo",
        "severe": "Nghiêm trọng",
        "flood_warning": "Cảnh báo lũ lụt",
        "normal_message": "Tất cả các thông số đều trong phạm vi bình thường.",
        "watch_message": "Một số thông số cho thấy nguy cơ tiềm ẩn. Theo dõi tình hình.",
        "warning_message": "Cảnh báo! Nguy cơ lũ lụt đang tăng cao. Hãy chuẩn bị.",
        "severe_message": "Cảnh báo nghiêm trọng! Nguy cơ lũ lụt cao. Hãy hành động ngay lập tức."
    }
}



def save_global_data(data: SensorData):
    if data is None:
        return
    
    global sensor_data_history

    data.rainfall = str(data.rainfall)
    data.soil_humidity = str(data.soil_humidity)
    data.air_humidity = float(data.air_humidity)
    data.air_pressure = float(data.air_pressure)
    data.temperature = float(data.temperature)
    data.water_level = float(data.water_level)

    new_data_global = SensorData(
        timestamp = datetime.now(),
        temperature = data.temperature,
        air_pressure= data.air_pressure,
        air_humidity = data.air_humidity,
        rainfall = data.rainfall,
        soil_humidity = data.soil_humidity,
        water_level = data.water_level
    )

    sensor_data_history.append(new_data_global)
    if len(sensor_data_history) > MAX_HISTORY_SIZE:
            sensor_data_history.pop(0)


def get_current_data():
    global sensor_data_history, current_warning_level, current_language
    
    if not sensor_data_history:
        # Return default values if no data is available
        return JSONResponse(content={
            "timestamp": datetime.now().isoformat(),
            "rainfall": 0,
            "soil_humidity": 0,
            "air_humidity": 0,
            "air_pressure": 0,
            "temperature": 0,
            "water_level": 0,
            "warning_level": "No Data",
            "language": current_language
        })
    
    latest_data = sensor_data_history[-1]
    return JSONResponse(content={
        "timestamp": latest_data.timestamp.isoformat(),
        "rainfall": latest_data.rainfall,
        "soil_humidity": latest_data.soil_humidity,
        "air_humidity": latest_data.air_humidity,
        "air_pressure": latest_data.air_pressure,
        "temperature": latest_data.temperature,
        "water_level": latest_data.water_level,
        "warning_level": current_warning_level,
        "language": current_language
    })