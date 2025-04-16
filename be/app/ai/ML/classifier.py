from sklearn.linear_model import LogisticRegression
from ..Utils.utils import preprocess_text

class Classifier:
    def __init__(self, embedding):
        self.ml = LogisticRegression(max_iter=1000)
        self.embedding = embedding
        self.patterns = []
        self.tags = []
        self.responses = []

    def load_and_fit_patterns(self, flood_data: list):
        for item in flood_data:
            self.patterns.extend([preprocess_text(pattern) for pattern in item["patterns"]])
            self.tags.extend([item["tag"]] * len(item["patterns"]))
            self.responses.append(item["responses"])
        self.encoder_and_fit()
    def encoder_and_fit(self):
        if self.patterns:
            # Huấn luyện vectorizer và mô hình một lần khi tải dữ liệu
            patterns_embeddings = self.embedding.embed_documents(self.patterns)

            self.ml.fit(patterns_embeddings, self.tags)

    def classify_predict(self, user_input: str, threshold: float = 0.6) -> str:
        processed_input = preprocess_text(user_input)

        embedding_input = self.embedding.embed_query(processed_input)
        probabilities = self.ml.predict_proba([embedding_input])[0]

        # In xác suất của từng tag
        classes = self.ml.classes_
        for tag, prob in zip(classes, probabilities):
            print(f"{tag}: {prob:.4f}")

        # Trả về tag dự đoán
        pred_index = probabilities.argmax()
        pred_tag = self.ml.classes_[pred_index]  
        if probabilities[pred_index] > threshold:
            return pred_tag    

        return "unknow"
        
