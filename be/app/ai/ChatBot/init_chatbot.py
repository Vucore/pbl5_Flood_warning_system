from ..ML.classifier import Classifier
from .response_generator import ResponseGenerator
# from .message_history import MessageHistory
from ..Utils.data_loader import load_flood_data_local
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.agents import create_openai_tools_agent, AgentExecutor
from sentence_transformers import SentenceTransformer
import os
from ...services.handl_data_global import get_current_data_sensor
from .model_setup import load_local_gpt4all_model
class ChatbotBase:
    def __init__(self):
        self.llm = load_local_gpt4all_model()    

        self.intent_classifier = Classifier()
        self.response_generator = ResponseGenerator(self.llm)
        # self.message_history = MessageHistory()
        self.flood_data = load_flood_data_local()
        if self.flood_data:
            self.intent_classifier.load_and_fit_patterns(flood_data=self.flood_data)

    def generate_response(self, user_input: str, session_id="default_user") -> str:
        """Hàm sinh phản hồi từ người dùng"""
        # if not self.flood_data:
        #     self.load_data()  # Nếu flood data chưa được tải, tải lại

        pred_tag = self.intent_classifier.classify_predict(user_input)

        if pred_tag == "sensor_data":
            try:
                sensor_data = get_current_data_sensor()

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


        if pred_tag != "unknow" and pred_tag != "sensor_data":
            response = self.response_generator.generate_response_from_local(pred_tag, self.flood_data)
            # self.message_history.add_message(session_id, user_input, response)
            return response
        
        return "Tôi không chắc ý của bạn. Bạn có thể thử diễn đạt lại câu hỏi không?"
