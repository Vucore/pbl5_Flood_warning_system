from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
class TextSplitter():
    def __init__(self, 
                 separators: List[str] = [".", "\n\n", "\n", " ", ""],
                 chunk_size: int = 500,
                 chunk_overlap: int = 0
                 ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    def splitter_documents(self, documents):
        docs = self.splitter.split_documents(documents=documents)
        # for i, doc in enumerate(docs):
            # print(f"--- Document {i+1} ---")
            # print(doc.page_content)
            # print(doc.metadata)
            # print("\n")
        
        return docs
