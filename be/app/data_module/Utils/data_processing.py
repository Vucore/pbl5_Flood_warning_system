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

        if not (800 <= data.air_pressure <= 1100 or data.air_pressure == 0):
            raise ValueError("Air pressure out of range")
        
        if not (0 <= data.water_level <= 100):
            raise ValueError("Water level out of range")

        if not (0 <= data.rainfall <= 50):
            raise ValueError("Rain fall out of range")
        
        return data  
    except ValueError as e:
        print(f"Data validation error: {e}")
        return None  # Trả về None nếu dữ liệu không hợp lệ

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