from sklearn.linear_model import LogisticRegression
from ..Utils.utils import preprocess_text

class Classifier:
    def __init__(self, embedding):
        self.ml_question = LogisticRegression(max_iter=1000)
        self.ml_context = LogisticRegression(max_iter=1000)
        self.embedding = embedding

    def setup_question_classifier(self, flood_data: list):
        patterns = []
        tags = []
        responses = []
        for item in flood_data:
            patterns.extend([preprocess_text(pattern) for pattern in item["patterns"]])
            tags.extend([item["tag"]] * len(item["patterns"]))
            responses.append(item["responses"])
        self.embedding_and_fit(patterns, tags, 1)
    
    def setup_context_RAG_classsifier(self, context_sample: list):
        patterns = []
        tags = []
        for item in context_sample:
            patterns.extend([preprocess_text(pattern) for pattern in item["patterns"]])
            tags.extend([item["tag"]] * len(item["patterns"]))
        self.embedding_and_fit(patterns, tags, 2)

    '''
        Mode 1: Dành cho mô hình phân loại trả lời câu hỏi
        Mode 2: Dành cho phân loại ngữ cảnh RAG
    '''
    def embedding_and_fit(self, patterns, tags, mode: int):
        if patterns:
            # Huấn luyện vectorizer và mô hình một lần khi tải dữ liệu
            patterns_embeddings = self.embedding.embed_documents(patterns)
            if 1 == mode:
                self.ml_question.fit(patterns_embeddings, tags)
            elif 2 == mode:
                self.ml_context.fit(patterns_embeddings, tags)

    def classify_predict_tag(self, user_input: str, mode: int, threshold: float = 0.4) -> str:
        processed_input = preprocess_text(user_input)

        embedding_input = self.embedding.embed_query(processed_input)

        if 1 == mode:
            probabilities = self.ml_question.predict_proba([embedding_input])[0]

            # In xác suất của từng tag
            classes = self.ml_question.classes_
            for tag, prob in zip(classes, probabilities):
                print(f"{tag}: {prob:.4f}")

            # Trả về tag dự đoán
            pred_index = probabilities.argmax()
            pred_tag = self.ml_question.classes_[pred_index]  
            if probabilities[pred_index] > threshold:
                return pred_tag    

            return "unknow"
        
        elif 2 == mode:
            probabilities = self.ml_context.predict_proba([embedding_input])[0]
            pred_index = probabilities.argmax()
            pred_tag = self.ml_context.classes_[pred_index]  
            return pred_tag    

    