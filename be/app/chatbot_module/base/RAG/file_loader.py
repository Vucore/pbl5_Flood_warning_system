from langchain_community.document_loaders import PyPDFLoader
from ..Utils.path_loader import get_path_pdf_data

class PDFLoader():
    def __init__(self):
        self.pdf_path = get_path_pdf_data('Thong_tin_lu_lut_Viet_Nam.pdf')
    def load_docs(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()    
        return documents
    