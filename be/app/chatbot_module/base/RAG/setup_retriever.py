from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

class Retriever():
    def __init__(self, retriever_class = BM25Retriever):
        self.retriever_class = retriever_class

    def build_retriever(self, docs, k: int):
        retriever = self.retriever_class.from_documents(documents=docs)
        retriever.k = k
        return retriever
    
    def get_ensemble_retriever(self,
                      search_type:str = "similarity",
                      search_kwargs: dict = {"k": 4},
                      vectorstore = None,
                      retriever = None
                    ):
  
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                        vectorstore.as_retriever(
                                            search_type=search_type,
                                            search_kwargs=search_kwargs
                                            ), 
                        retriever
                        ],
                        weights=[0.7, 0.3],
        )
        return ensemble_retriever   