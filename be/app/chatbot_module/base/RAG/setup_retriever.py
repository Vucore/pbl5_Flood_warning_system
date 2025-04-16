from langchain_community.retrievers import BM25Retriever

class Retriever():
    def __init__(self, retriever_class = BM25Retriever):
        self.retriever_class = retriever_class

    def build_retriever(self, documents, k):
        retriever = self.retriever_class.from_documents(documents=documents)
        retriever.k = k
        return retriever