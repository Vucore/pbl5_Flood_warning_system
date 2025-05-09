from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from typing import List
from ..Utils.get_path_file import get_path_and_name_pdf_data

class PDFLoader():
    def __init__(self):
        self.pdf_paths, self.doc_name = get_path_and_name_pdf_data()
    # def load_docs(self):
    #     loader = PyPDFLoader(self.pdf_path)
    #     documents = loader.load()    
    #     return documents
    def load_docs(self) -> List[Document]:
        documents = []
        for i, path in enumerate(self.pdf_paths):
            loader = PyPDFLoader(path)
            pages = loader.load() 
            combined_content = "\n".join([page.page_content for page in pages])
            doc = Document(
                page_content=combined_content, 
                metadata={
                    "source": str(path), 
                    "doc_name": str(self.doc_name[i])} 
            )
            documents.append(doc)
        return documents