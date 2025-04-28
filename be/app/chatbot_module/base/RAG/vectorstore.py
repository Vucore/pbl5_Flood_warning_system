from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
import hashlib

class VectorDB:
    def __init__(self,
                 docs = None,
                 embedding = None,
                 ) -> None:
        self.docs = docs
        self.embedding = embedding
        self.vectorstore = None

    def generate_unique_id(self, document):
        text = document.page_content 
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def get_vectorstore(self):
        uuids = [self.generate_unique_id(doc) for doc in self.docs]
        self.vectorstore = Chroma(
            collection_name="chroma_db",
            embedding_function=self.embedding,
            persist_directory="./chroma_db",
        )
        self.vectorstore.add_documents(
                            documents=self.docs, 
                            ids=uuids)
        return self.vectorstore
    
    
    # def __build_db(self, docs):
    #     # def normalize_score(score):
    #     #     # Ví dụ: clip score vào khoảng [0, 1]
    #     #     return max(0.0, min(1.0, score))

    #     db = self.vector_db.from_documents(
    #         embedding=self.embedding,
    #         documents=docs,
    #         # relevance_score_fn=normalize_score  # Thêm dòng này
    #     )
        
    #     return db

    # def get_ensemble_retriever(self,
    #                   search_type:str = "similarity",
    #                   search_kwargs: dict = {"k": 10}
    #                 ):
  
    #     ensemble_retriever = EnsembleRetriever(
    #         retrievers=[
    #                     self.db.as_retriever(
    #                                         # search_type="similarity_score_threshold", 
    #                                         # search_kwargs = { "k": 10, "score_threshold": 0.6 }
    #                                         search_type=search_type,
    #                                         search_kwargs=search_kwargs
    #                                         ), 
    #                     self.retriever_class.build_retriever(self.documents, 5)
    #                     ],
    #                     weights=[0.7, 0.3],
    #     )
    #     return ensemble_retriever           
