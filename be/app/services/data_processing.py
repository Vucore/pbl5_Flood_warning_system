# app/services/data_processing.py
from ..database.SensorData import SensorData


def clean_and_validate_data(data: SensorData):
    """
    Làm sạch và kiểm tra dữ liệu sensor trước khi lưu vào database.
    """
    try:
        # Chuyển đổi dữ liệu sang kiểu số
        data.rainfall = float(data.rainfall)
        data.soil_humidity = float(data.soil_humidity)
        data.air_humidity = float(data.air_humidity)
        data.air_pressure = float(data.air_pressure)
        data.temperature = float(data.temperature)
        data.water_level = float(data.water_level)

        #đảo ngược 2 giá trị
        # Kiểm tra giá trị hợp lệ (ví dụ: nhiệt độ không thể < 0 hoặc > 100)
        if not (0 <= data.temperature <= 100):
            raise ValueError("Temperature out of range")
        
        if not (0 <= data.air_humidity <= 100):
            raise ValueError("Air humidity out of range")

        if not (0 <= data.soil_humidity <= 1024):
            raise ValueError("Soil humidity out of range")

        if not (800 <= data.air_pressure <= 1100):
            raise ValueError("Air pressure out of range")
        
        if not (0 <= data.water_level <= 100):
            raise ValueError("Water level out of range")

        if not (0 <= data.rainfall <= 1024):
            raise ValueError("Rain fall out of range")
        
        data.rainfall = invert_sensor_value(data.rainfall)
        data.soil_humidity = invert_sensor_value(data.soil_humidity)

        data.rainfall = classify_rainfall(data.rainfall)
        data.soil_humidity = classify_soil_humidity(data.soil_humidity)

        return data  
    except ValueError as e:
        print(f"Data validation error: {e}")
        return None  # Trả về None nếu dữ liệu không hợp lệ
    
def invert_sensor_value(value, max_value=1024):
    """Đảo ngược giá trị cảm biến trong phạm vi [0, max_value]."""
    return max_value - value

def classify_rainfall(rainfall: float) -> str:
    """
    Phân loại lượng mưa dựa vào giá trị mm.
    """
    if rainfall <= 0:
        return "Không có mưa"
    elif rainfall <= 400:
        return "Mưa nhỏ"
    elif rainfall <= 700:
        return "Mưa vừa"
    elif rainfall <= 900:
        return "Mưa to"
    else:
        return "Mưa rất to"

def classify_soil_humidity(soil_humidity:float) -> str:
    if soil_humidity >= 700:
        return "Ẩm"
    elif soil_humidity >= 301:
        return "Bình thường"
    else:
        return "Khô"
    
def convert_to_json(data: SensorData):
    """
    Chuyển đổi đối tượng SensorData thành chuỗi JSON
    """
    if data is not None:
        return data.model_dump_json()
    else:
        print("⚠ Lỗi: data bị None!")
        return None

def convert_message_to_sensor_data(message: str):
    parts = message.split(";")
    temperature = float(parts[0].strip())
    air_pressure = float(parts[1].strip())
    air_humidity = float(parts[2].strip())
    rainfall = float(parts[3].strip())
    soil_humidity = float(parts[4].strip())
    water_level = float(parts[5].strip())


    sensor_data = SensorData(timestamp=None,
                            rainfall = rainfall,
                            soil_humidity = soil_humidity, 
                            air_humidity = air_humidity, 
                            air_pressure= air_pressure, 
                            temperature = temperature, 
                            water_level = water_level)
    return sensor_data