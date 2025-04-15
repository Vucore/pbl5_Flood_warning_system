from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from .retriever import Retriever
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
        self.db = self.__build_db(documents)
        self.retriever_class = Retriever()
   
    def __build_db(self, docs):
        db = self.vector_db.from_documents(documents=self.docs, embedding=self.embedding)
        return db

    def get_ensemble_retriever(self,
                      search_type:str = "similarity",
                      search_kwargs: dict = {"k": 10}
                    ):
  
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                        self.db.as_retriever(
                                            search_type="similarity_score_threshold", 
                                            search_kwargs = { "k": 10, "score_threshold": 0.8 }
                                            ), 
                        self.retriever_class.build_retriever(self.documents, 4)
                        ],
                        weights=[0.7, 0.3],
        )
        return ensemble_retriever           