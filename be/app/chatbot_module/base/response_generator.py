import random
from ...data_module.Utils.global_state import GlobalState

class ResponseGenerator:
    def __init__(self, agent):
        self.agent = agent

    def generate_response_from_local(self, intent: str, flood_data: list) -> str:
        for item in flood_data:
            if item["tag"] == intent:
                return random.choice(item["responses"])
        return "Dữ liệu không đủ để trả lời câu hỏi của bạn."

    def generate_response_sensor_data(self):
        try:
            sensor_data = GlobalState.get_current_data_sensor()
            print(sensor_data)
            air_humidity = float(sensor_data.get('air_humidity', 0))
            air_pressure = float(sensor_data.get('air_pressure', 0))
            temperature = float(sensor_data.get('temperature', 0))
            water_level = float(sensor_data.get('water_level', 0))

            return (f"Chỉ số cảm biến hiện tại:\n"
                    f"• Hiện tại: {sensor_data['timestamp']}\n"
                    f"• Lượng mưa: {sensor_data['rainfall']}\n"
                    f"• Độ ẩm đất: {sensor_data['soil_humidity']}\n"
                    f"• Độ ẩm không khí: {air_humidity:.2f}%\n"
                    f"• Áp suất không khí: {air_pressure:.2f}hPa\n"
                    f"• Nhiệt độ: {temperature:.2f}°C\n"
                    f"• Mực nước: {water_level:.2f}m\n"
                    f"• Mức độ nguy hiểm: {sensor_data['warning_level']}\n")
                
        except Exception as e:
            return f"Lỗi khi lấy dữ liệu cảm biến: {str(e)}. Vui lòng thử lại sau."
        
    def generate_agent_response(self, message):
        return self.agent.run(message)