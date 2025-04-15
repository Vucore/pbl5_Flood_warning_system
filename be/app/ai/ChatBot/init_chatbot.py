from fastapi.responses import StreamingResponse
from ..ML.embedding import CustomVietnameseEmbedding
from ..ML.classifier import Classifier
from ..Utils.data_loader import load_flood_data_local
from .response_generator import ResponseGenerator
from .model_setup import load_model_Llama3
from .Agent.agent import Agent
import asyncio

class ChatbotBase:
    def __init__(self):
        self.llm = load_model_Llama3()
        self.embedding = CustomVietnameseEmbedding()
        self.intent_classifier = Classifier(self.embedding)
        self.agent = Agent(self.llm, self.embedding)
        self.response_generator = ResponseGenerator(self.agent)

        self.flood_data = load_flood_data_local()
        if self.flood_data:
            self.intent_classifier.load_and_fit_patterns(flood_data=self.flood_data)

    def generate_response(self, user_input: str, session_id="default_user") -> str:
        """Hàm sinh phản hồi từ người dùng"""
        pred_tag = self.intent_classifier.classify_predict(user_input)

        async def stream_answer(answer: str):
            try:
                for char in answer:
                    yield char
                    await asyncio.sleep(0.002)
            except Exception as e:
                yield f"ERROR: {str(e)}"

        if pred_tag == "sensor_data":
            answer = self.response_generator.generate_response_sensor_data()
            return StreamingResponse(stream_answer(answer=answer), media_type="text/plain; charset=utf-8")

        elif pred_tag != "unknow" and pred_tag != "sensor_data":
            answer = self.response_generator.generate_response_from_local(pred_tag, self.flood_data)
            return StreamingResponse(stream_answer(answer=answer), media_type="text/plain; charset=utf-8")
        else:         
            return self.response_generator.generate_agent_response(user_input)