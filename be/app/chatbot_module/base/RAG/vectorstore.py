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