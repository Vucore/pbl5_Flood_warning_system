import random
from sklearn.linear_model import LogisticRegression
from ..Utils.utils import preprocess_text
from ..ChatBot.model_setup import load_vietnamese_encoder_model
import torch
class Classifier:
    def __init__(self):
        self.ml = LogisticRegression(max_iter=1000)
        self.tokenizer, self.encoder_model = load_vietnamese_encoder_model()
        self.patterns = []
        self.tags = []
        self.responses = []

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


    def load_and_fit_patterns(self, flood_data: list):
        for item in flood_data:
            self.patterns.extend([preprocess_text(pattern) for pattern in item["patterns"]])
            self.tags.extend([item["tag"]] * len(item["patterns"]))
            self.responses.append(item["responses"])
        self.encoder_and_fit()
    def encoder_and_fit(self):
        if self.patterns:
            # Huấn luyện vectorizer và mô hình một lần khi tải dữ liệu
            # Tokenize sentences
            encoded_patterns = self.tokenizer(self.patterns, padding=True, truncation=True, return_tensors='pt')

            # Compute token embeddings
            with torch.no_grad():
                model_output = self.encoder_model(**encoded_patterns)

            # Perform pooling. In this case, mean pooling.
            patterns_embeddings = self.mean_pooling(model_output, encoded_patterns['attention_mask'])
            
            self.ml.fit(patterns_embeddings, self.tags)

    def classify_predict(self, user_input: str, threshold: float = 0.75) -> str:
        processed_input = preprocess_text(user_input)

        encoded_input = self.tokenizer(processed_input, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
                model_output = self.encoder_model(**encoded_input)
         # Perform pooling. In this case, mean pooling.
        input_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        # Dự đoán xác suất intent
        probabilities = self.ml.predict_proba(input_embeddings)[0]


        # In xác suất của từng tag
        classes = self.ml.classes_
        for tag, prob in zip(classes, probabilities):
            print(f"{tag}: {prob:.4f}")

        # Trả về tag dự đoán
        pred_index = probabilities.argmax()
        pred_tag = self.ml.classes_[pred_index]  
        if probabilities[pred_index] > 0.5:
            return pred_tag    

        return "unknow"
        
