# be/app/data_module/global_state.py
from datetime import datetime
from ..database.SensorData import SensorData

MAX_HISTORY_SIZE = 288

class GlobalState:
    sensor_data_history = []

    @classmethod
    def save_global_data_sensor(cls, data: SensorData):
        if data is None:
            return

        data.rainfall = float(data.rainfall)
        data.soil_humidity = float(data.soil_humidity)
        data.air_humidity = float(data.air_humidity)
        data.air_pressure = float(data.air_pressure)
        data.temperature = float(data.temperature)
        data.water_level = float(data.water_level)

        new_data_global = SensorData(
            timestamp=datetime.now(),
            temperature=data.temperature,
            air_pressure=data.air_pressure,
            air_humidity=data.air_humidity,
            rainfall=data.rainfall,
            soil_humidity=data.soil_humidity,
            water_level=data.water_level
        )

        cls.sensor_data_history.append(new_data_global)
        if len(cls.sensor_data_history) > MAX_HISTORY_SIZE:
            cls.sensor_data_history.pop(0)

    @classmethod
    def get_current_data_sensor(cls):
        if not cls.sensor_data_history:
            return {
                "timestamp": datetime.now().isoformat(),
                "rainfall": 0,
                "soil_humidity": 0,
                "air_humidity": 0,
                "air_pressure": 0,
                "temperature": 0,
                "water_level": 0
            }

        latest_data = cls.sensor_data_history[-1]

        if isinstance(latest_data.timestamp, str):
            timestamp_str = latest_data.timestamp
        else:
            timestamp_str = latest_data.timestamp.isoformat()

        return {
            "timestamp": timestamp_str,
            "rainfall": latest_data.rainfall,
            "soil_humidity": latest_data.soil_humidity,
            "air_humidity": latest_data.air_humidity,
            "air_pressure": latest_data.air_pressure,
            "temperature": latest_data.temperature,
            "water_level": latest_data.water_level,
        }
