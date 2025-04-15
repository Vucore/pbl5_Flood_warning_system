from langchain_community.chat_models import ChatOllama
from fastapi.responses import StreamingResponse
from ..ML.classifier import Classifier
from ..ML.embedding import CustomVietnameseEmbedding
from ..Utils.data_loader import load_flood_data_local
from .response_generator import ResponseGenerator
from .agent import Agent
import asyncio

class ChatbotBase:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.1)   
        self.embedding = CustomVietnameseEmbedding()
        self.intent_classifier = Classifier(self.embedding)
        self.agent = Agent(self.llm)
        self.response_generator = ResponseGenerator(self.agent)

        self.flood_data = load_flood_data_local()
        if self.flood_data:
            self.intent_classifier.load_and_fit_patterns(flood_data=self.flood_data)

    # def get_agent_response(self, message):
    #     agent = self.agent
    #     return agent.run(message)

    def generate_response(self, user_input: str, session_id="default_user") -> str:
        """Hàm sinh phản hồi từ người dùng"""
        pred_tag = self.intent_classifier.classify_predict(user_input)

        if pred_tag == "sensor_data":
            async def generate():
                answer = self.response_generator.generate_response_sensor_data()
                for char in answer:
                    yield char
                    await asyncio.sleep(0.002)

            return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")

        if pred_tag != "unknow" and pred_tag != "sensor_data":
            async def generate():
                    answer = self.response_generator.generate_response_from_local(pred_tag, self.flood_data)
                    for char in answer:
                        yield char
                        await asyncio.sleep(0.002)

            return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")

        return self.response_generator.generate_agent_response(user_input)
