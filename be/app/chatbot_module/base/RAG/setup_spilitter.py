from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from typing import List

class TextSplitter():
    def __init__(self,
                 chunk_size: int = 500,
                 chunk_overlap: int = 0
                 ) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=[".", "\n\n", "\n", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        # Splitter cho markdown
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "heading1"),
                ("##", "heading2"),
                ("###", "heading3"),
            ]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        split_docs = []
        
        for doc in documents:
            if doc.metadata.get("type") == "markdown":
                # Split markdown theo tiêu đề
                md_splits = self.markdown_splitter.split_text(doc.page_content)
                # Chuyển đổi các phần split thành Document với metadata gốc
                for split in md_splits:
                    clean_content = split.page_content
                    clean_content = clean_content.replace("*", "")
                    clean_content = clean_content.replace("-", "")
                    clean_content = clean_content.strip() 
                    split_doc = Document(
                        page_content=clean_content,
                        metadata={
                            **doc.metadata,
                            **split.metadata  # Thêm thông tin heading
                        }
                    )
                    split_docs.append(split_doc)
            else:
                # Sử dụng text splitter thông thường cho các tài liệu khác
                splits = self.text_splitter.split_documents([doc])
                split_docs.extend(splits)
        # In thông tin debug
        # for i, doc in enumerate(split_docs):
        #     print(f"\n--- Document Chunk {i+1} ---")
        #     print(f"Content length: {len(doc.page_content)}")
        #     print(f"COntent: {doc.page_content}" )
        #     print(f"Metadata: {doc.metadata}")
        #     print("-" * 50)
        
        return split_docs


# class TextSplitter():
#     def __init__(self, 
#                  separators: List[str] = [".", "\n\n", "\n", " ", ""],
#                  chunk_size: int = 500,
#                  chunk_overlap: int = 0
#                  ) -> None:
#         self.splitter = RecursiveCharacterTextSplitter(
#             separators=separators,
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap
#         )
#     def splitter_documents(self, documents):
#         docs = self.splitter.split_documents(documents=documents)
        
#         # for i, doc in enumerate(docs):
#             # print(f"--- Document {i+1} ---")
#             # print(doc.page_content)
#             # print(doc.metadata)
#             # print("\n")
        
#         return docs
