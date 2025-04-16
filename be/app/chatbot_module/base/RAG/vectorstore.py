from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from .setup_retriever import Retriever

class VectorDB:
    def __init__(self,
                 documents = None,
                 docs = None,
                 vector_db = FAISS,
                 embedding = None,
                 ) -> None:
        self.documents = documents
        self.docs = docs
        self.vector_db = vector_db
        self.embedding = embedding
        self.db = self.__build_db(docs)
        self.retriever_class = Retriever()
   
    def __build_db(self, docs):
        # def normalize_score(score):
        #     # Ví dụ: clip score vào khoảng [0, 1]
        #     return max(0.0, min(1.0, score))

        db = self.vector_db.from_documents(
            documents=docs,
            embedding=self.embedding,
            # relevance_score_fn=normalize_score  # Thêm dòng này
        )
        return db

    def get_ensemble_retriever(self,
                      search_type:str = "similarity",
                      search_kwargs: dict = {"k": 10}
                    ):
  
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                        self.db.as_retriever(
                                            # search_type="similarity_score_threshold", 
                                            # search_kwargs = { "k": 10, "score_threshold": 0.6 }
                                            search_type=search_type,
                                            search_kwargs=search_kwargs
                                            ), 
                        self.retriever_class.build_retriever(self.documents, 5)
                        ],
                        weights=[0.7, 0.3],
        )
        return ensemble_retriever           