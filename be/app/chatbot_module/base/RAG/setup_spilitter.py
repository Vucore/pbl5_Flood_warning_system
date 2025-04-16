from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
class TextSplitter():
    def __init__(self, 
                 separators: List[str] = ["\n\n", "\n", " ", ""],
                 chunk_size: int = 500,
                 chunk_overlap: int = 50
                 ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    def splitter_documents(self, documents):
        docs = self.splitter.split_documents(documents=documents)
        return docs
