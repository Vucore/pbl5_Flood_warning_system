from langchain.embeddings.base import Embeddings
from ..model_setup import load_vietnamese_encoder_model
import torch

class CustomVietnameseEmbedding(Embeddings):
    def __init__(self):
        self.tokenizer, self.encoder_model = load_vietnamese_encoder_model()

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embedding(self, texts):
        result = []
        for text in texts:
            encoded_text = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                model_output = self.encoder_model(**encoded_text)
            text_embeddings = self.mean_pooling(model_output, encoded_text['attention_mask'])
            result.append(text_embeddings.squeeze(0).numpy())
        return result

    def embed_documents(self, texts):
        return self.embedding(texts)

    def embed_query(self, text):
        return self.embedding([text])[0]

#         # num_vectors = vectorstore.index.ntotal
#         # print(f"📦 Tổng số vector trong FAISS: {num_vectors}")

#         # retrieved_docs = vectorstore.docstore._dict  # Dict lưu mapping ID -> Document

#         # for i in range(num_vectors):
#         #     vector = vectorstore.index.reconstruct(i)  # Lấy vector theo index
#         #     doc_id = list(retrieved_docs.keys())[i]   # ID tài liệu
#         #     doc = retrieved_docs[doc_id]              # Tài liệu văn bản

#         #     print(f"\n📄 Document #{i + 1}:")
#         #     print(f"🧾 Nội dung: {doc.page_content[:200]}...")  # In 200 ký tự đầu
#         #     print(f"🔢 Vector (len={len(vector)}): {vector[:10]}...")  # In 10 phần tử đầu

