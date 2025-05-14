from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
from typing import List
from ..Utils.get_path_file import get_path_and_name_pdf_data, get_path_and_name_markdown_data

class DocumentLoader():
    def __init__(self):
        self.pdf_paths, self.doc_names = get_path_and_name_pdf_data()
        self.markdown_paths, self.markdown_names = get_path_and_name_markdown_data()

    def load_pdf_docs(self) -> List[Document]:
        documents = []
        for i, path in enumerate(self.pdf_paths):
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
                pages = loader.load() 
                combined_content = "\n".join([page.page_content for page in pages])
                doc = Document(
                    page_content=combined_content, 
                    metadata={
                        "source": str(path), 
                        "doc_name": str(self.doc_names[i]),
                        "type": "pdf"
                    }
                )
                documents.append(doc)
        return documents
    
    def load_markdown_docs(self) -> List[Document]:
        documents = []
        for i, path in enumerate(self.markdown_paths):
            try:
                loader = TextLoader(path, encoding="utf-8")
                docs = loader.load()
                for doc in docs:
                    doc.metadata.update({
                        "source": str(path),
                        "doc_name": str(self.markdown_names[i]),
                        "type": "markdown"
                    })
                documents.extend(docs)
                print(f"Loaded markdown file: {self.markdown_names[i]}")
            except Exception as e:
                print(f"Lỗi khi đọc file markdown {path}: {e}")
        return documents