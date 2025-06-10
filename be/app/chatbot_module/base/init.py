from fastapi.responses import StreamingResponse
from .ML.embedding import CustomVietnameseEmbedding
from .ML.classifier import Classifier
from .Utils.get_path_file import load_json_local_data
from .response_generator import ResponseGenerator
from .model_setup import load_model_Llama3
from .Agent.rag_agent import RAGAgent
from .Agent.email_agent import EmailAgent 
from .Utils.conversation_logger import ConversationLogger

import asyncio

class ChatbotBase:
    def __init__(self):
        self.llm = load_model_Llama3()
        self.embedding = CustomVietnameseEmbedding()
        self.classifier = Classifier(self.embedding)
        self.rag_agent = RAGAgent(self.llm, self.embedding)
        self.email_agent = EmailAgent()
        self.response_generator = ResponseGenerator(self.rag_agent, self.email_agent)
        self.conversation_logger = ConversationLogger()

        self.flood_data = load_json_local_data("responses.json")
        if self.flood_data:
            self.classifier.setup_question_classifier(flood_data=self.flood_data)

        self.context_RAG_sample = load_json_local_data("context.json")
        if self.context_RAG_sample:
            self.classifier.setup_context_RAG_classsifier(context_sample=self.context_RAG_sample)

    def generate_response_noRAG(self, user_input: str, session_id="default_user") -> str:
        """Hàm sinh phản hồi từ người dùng dựa theo json"""
        pred_tag = self.classifier.classify_predict_tag(user_input=user_input, mode=1, threshold=0.4)

        async def stream_answer(answer: str):
            try:
                for char in answer:
                    yield char
                    await asyncio.sleep(0.002)
            except Exception as e:
                yield f"ERROR: {str(e)}"

        if pred_tag == "sensor_data":
            answer = self.response_generator.generate_response_sensor_data()
            # Log the conversation
            self.conversation_logger.log_conversation(
                question=user_input,
                answer=answer,
                rag_used=False,
                response_type="sensor_data"
            )
            return StreamingResponse(stream_answer(answer=answer), media_type="text/plain; charset=utf-8")

        elif pred_tag != "unknow" and pred_tag != "sensor_data":
            answer = self.response_generator.generate_response_from_local(pred_tag, self.flood_data)
            # Log the conversation
            self.conversation_logger.log_conversation(
                question=user_input,
                answer=answer,
                rag_used=False,
                response_type=pred_tag
            )
            return StreamingResponse(stream_answer(answer=answer), media_type="text/plain; charset=utf-8")
        else:         
            answer = "Tôi không hiểu câu hỏi, vui lòng cung cấp thêm thông tin!"
            # Log the conversation
            self.conversation_logger.log_conversation(
                question=user_input,
                answer=answer,
                rag_used=False,
                response_type="unknown"
            )
            return StreamingResponse(stream_answer(answer=answer), media_type="text/plain; charset=utf-8")
        
   
   
    def generate_response_RAG(self, user_input: str, session_id="default_user") -> str:
        """Hàm sinh phản hồi từ người dùng bằng mô hình Llama3"""
        question_type = self.classifier.classify_predict_tag(user_input=user_input, mode=2, threshold=0)
        question_type = question_type.strip().lower()
        print(question_type)
        if 'simple' in question_type:
            return self.response_generator.generate_RAGagent_response(user_input)
        elif 'chat' in question_type:
            return self.response_generator.generate_llm_response(user_input)
        elif 'call' in question_type:
            result = self.response_generator.call_email_agent()
            async def stream_answer(answer: str):
                try:
                    for char in answer:
                        yield char
                        await asyncio.sleep(0.002)
                except Exception as e:
                    yield f"ERROR: {str(e)}"
            return StreamingResponse(stream_answer(answer=result), media_type="text/plain; charset=utf-8")
   
   
   
   
   
   
    '''Adaptive RAG with LLM'''
    # def generate_response_RAG(self, user_input: str, session_id="default_user") -> str:
    #     question_type = query_classifier.invoke(user_input)
    #     question_type = question_type.strip().lower()
    #     print(question_type)
    #     if 'simple' in question_type:
    #         return self.response_generator.generate_RAGagent_response(user_input)
    #     elif 'chat' in question_type:
    #         return self.response_generator.generate_llm_response(user_input)
    #     elif 'call' in question_type:
    #         result = self.response_generator.call_email_agent()
    #         async def stream_answer(answer: str):
    #             try:
    #                 for char in answer:
    #                     yield char
    #                     await asyncio.sleep(0.002)
    #             except Exception as e:
    #                 yield f"ERROR: {str(e)}"
    #         return StreamingResponse(stream_answer(answer=result), media_type="text/plain; charset=utf-8")

