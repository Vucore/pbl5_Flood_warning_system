# app/services/data_processing.py
from ..database.SensorData import SensorData


def clean_and_validate_data(data: SensorData):
    """
    Làm sạch và kiểm tra dữ liệu sensor trước khi lưu vào database.
    """
    try:
        try:
            data = SensorData(
                timestamp=data.timestamp,
                rainfall=float(str(data.rainfall).strip()),
                soil_humidity=float(str(data.soil_humidity).strip()),
                air_humidity=float(str(data.air_humidity).strip()),
                air_pressure=float(str(data.air_pressure).strip()),
                temperature=float(str(data.temperature).strip()),
                water_level=float(str(data.water_level).strip())
            )
        except ValueError as e:
            print(f"Type conversion error: {e}")
            return None

        #đảo ngược 2 giá trị
        # Kiểm tra giá trị hợp lệ (ví dụ: nhiệt độ không thể < 0 hoặc > 100)
        if not (0 <= data.temperature <= 100):
            raise ValueError("Temperature out of range")
        
        if not (0 <= data.air_humidity <= 100):
            raise ValueError("Air humidity out of range")

        if not (0 <= data.soil_humidity <= 100):
            raise ValueError("Soil humidity out of range")

        if not (800 <= data.air_pressure <= 1100):
            raise ValueError("Air pressure out of range")
        
        if not (0 <= data.water_level <= 100):
            raise ValueError("Water level out of range")

        if not (0 <= data.rainfall <= 1024):
            raise ValueError("Rain fall out of range")
        
        data.rainfall = float(convert_rain_to_mm_per_hour(sensor_value=data.rainfall))
        return data  
    except ValueError as e:
        print(f"Data validation error: {e}")
        return None  # Trả về None nếu dữ liệu không hợp lệ


def convert_rain_to_mm_per_hour(sensor_value, min_value=650, max_value=1000, max_rain_rate=20):
    if sensor_value == 0:
        return 0
    try:
        # Ensure all values are float
        sensor_value = float(str(sensor_value).strip())
        min_value = float(min_value)
        max_value = float(max_value)
        max_rain_rate = float(max_rain_rate)
        
        # Calculate with validated float values
        rate = ((max_value - sensor_value) / (max_value - min_value)) * max_rain_rate
        # Ensure return value is float
        return 0.0 if rate < 0 else float(rate)
    except (ValueError, TypeError) as e:
        print(f"Rain conversion error: {e}")
        return 0.0
    
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