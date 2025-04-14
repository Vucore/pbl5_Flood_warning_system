import random

class ResponseGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_response_from_local(self, intent: str, flood_data: list) -> str:
        for item in flood_data:
            if item["tag"] == intent:
                return random.choice(item["responses"])
        return "Dữ liệu không đủ để trả lời câu hỏi của bạn."
