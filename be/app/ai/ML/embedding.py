
# from langchain.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS  
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.retrievers import EnsembleRetriever
# from langchain_community.retrievers import BM25Retriever
# from langchain.embeddings.base import Embeddings
# from ..Utils.data_loader import get_path_pdf_data
# from ..ChatBot.model_setup import load_vietnamese_encoder_model
# import torch


# class CustomVietnameseEmbedding(Embeddings):
#     def __init__(self):
#         self.tokenizer, self.encoder_model = load_vietnamese_encoder_model()
#         self.pdf_path = get_path_pdf_data('Thong_tin_lu_lut_Viet_Nam.pdf')
#         self.retriever = self.__setup_retriever()
#     def mean_pooling(self, model_output, attention_mask):
#         token_embeddings = model_output[0] #First element of model_output contains all token embeddings
#         input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
#         return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
#     def embedding(self, texts):
#         result = []
#         if texts:
#             for text in texts:
#                 # Tokenize sentences
#                 encoded_text = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')

#                 # Compute token embeddings
#                 with torch.no_grad():
#                     model_output = self.encoder_model(**encoded_text)

#                 # Perform pooling. In this case, mean pooling.
#                 text_embeddings = self.mean_pooling(model_output, encoded_text['attention_mask'])
#                 result.append(text_embeddings.squeeze(0).numpy())
        
#         return result
    
#     def embed_documents(self, texts):
#         return self.embedding(texts)

#     def embed_query(self, text):
#         return self.embedding([text])[0]
    
#     def __getDocs(self):
#         loader = PyPDFLoader(self.pdf_path)
#         documents = loader.load()

#         # ==== Bước 2: Tách văn bản ====
#         text_splitter = RecursiveCharacterTextSplitter(
#             # separators = ["\n\n", "\n", " ", ".", ""],
#             chunk_size=500,
#             chunk_overlap=50)

#         docs = text_splitter.split_documents(documents)
#         return documents, docs
#     def __setup_retriever(self):
#         documents, docs = self.__getDocs()
#         # ==== Bước 3: Tạo embedding với BKAi ====
#         embedding_model = CustomVietnameseEmbedding()

#         # ==== Bước 4: Lưu vector vào FAISS ====
#         vectorstore = FAISS.from_documents(docs, embedding_model)
#         bm25_retriever = BM25Retriever.from_documents(documents)
#         bm25_retriever.k = 2 

#         ensemble_retriever = EnsembleRetriever(
#             retrievers=[vectorstore.as_retriever(), bm25_retriever],
#             weights=[0.8, 0.2],  # Bạn có thể điều chỉnh trọng số (weights) để ưu tiên retriever nào
#         )
#         return ensemble_retriever
#     def get_retriever(self):
#         return self.retriever


from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.embeddings.base import Embeddings
from ..Utils.data_loader import get_path_pdf_data
from ..ChatBot.model_setup import load_vietnamese_encoder_model
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


class VietnameseRetrieverBuilder:
    def __init__(self):
        self.pdf_path = get_path_pdf_data('Thong_tin_lu_lut_Viet_Nam.pdf')

    def load_docs(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(separators = ["\n\n", "\n", ".", ""], chunk_size=400, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        return documents, docs

    def build(self):
        documents, docs = self.load_docs()
        embedding_model = CustomVietnameseEmbedding()
        vectorstore = FAISS.from_documents(docs, embedding_model)
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 4

        # num_vectors = vectorstore.index.ntotal
        # print(f"📦 Tổng số vector trong FAISS: {num_vectors}")

        # retrieved_docs = vectorstore.docstore._dict  # Dict lưu mapping ID -> Document

        # for i in range(num_vectors):
        #     vector = vectorstore.index.reconstruct(i)  # Lấy vector theo index
        #     doc_id = list(retrieved_docs.keys())[i]   # ID tài liệu
        #     doc = retrieved_docs[doc_id]              # Tài liệu văn bản

        #     print(f"\n📄 Document #{i + 1}:")
        #     print(f"🧾 Nội dung: {doc.page_content[:200]}...")  # In 200 ký tự đầu
        #     print(f"🔢 Vector (len={len(vector)}): {vector[:10]}...")  # In 10 phần tử đầu

    

        ensemble_retriever = EnsembleRetriever(
            retrievers=[vectorstore.as_retriever(search_type="similarity_score_threshold", 
                                                 search_kwargs = { "k": 10, "score_threshold": 0.8 }
                                                ), 
                        bm25_retriever],
            weights=[0.7, 0.3],
        )
        return ensemble_retriever
