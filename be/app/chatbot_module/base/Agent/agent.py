from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from langchain.chains import RetrievalQA
from ..RAG.file_loader import PDFLoader
from ..RAG.spilitter import TextSplitter
from ..RAG.vectorstore import VectorDB
import asyncio
import functools
import logging

class Agent():
    def __init__(self, llm, embedding):
        self.llm = llm
        self.embedding = embedding
        self.pdf_loader = PDFLoader()
        self.splitter = TextSplitter()
        self.vectorstore = VectorDB(documents=self.pdf_loader.load_docs(), 
                                    docs=self.splitter.splitter_documents(self.pdf_loader.load_docs()),
                                    embedding=self.embedding,
                                    )
        self.retriever = self.vectorstore.get_ensemble_retriever()

        '''Agent'''
        # self.retriever_tool = create_retriever_tool(
        #     self.retriever,  
        #     "find_documents",
        #     "Find information in the text and answer questions."
        # )

        # self.tools = [self.retriever_tool]

        # Tạo prompt template
        # self.system_prompt = """Bạn là một trợ lý AI chuyên về cảnh báo lũ lụt, mực nước sông và lượng mưa hoặc các chỉ số thời tiết ở khu vực được cung cấp tài liệu.
        #                     Chỉ dựa vào thông tin tìm được từ công cụ và kiến thức nội tại của bạn về chủ đề này để trả lời.
        #                     Nếu không tìm thấy thông tin trong tài liệu, hãy nói rằng bạn không có thông tin đó trong tài liệu được cung cấp.
        #                     Luôn trả lời bằng tiếng Việt một cách rõ ràng và chi tiết nhất có thể dựa trên thông tin có được."""

        # self.prompt = ChatPromptTemplate.from_messages([
        #     ("system", self.system_prompt),
        #     ("human", "{input}"),
        #     MessagesPlaceholder(variable_name="agent_scratchpad")
        # ])

        # # Tạo agent từ LLM, prompt và tools
        # self.agent = create_openai_functions_agent(
        #                 llm=self.llm, 
        #                 tools=self.tools, 
        #                 prompt=self.prompt)

        # # Tạo agent executor để sử dụng
        # self.executor = AgentExecutor(
        #                 agent=self.agent, 
        #                 tools=self.tools, 
        #                 verbose=True,
        #                 handle_parsing_errors=True)
        '''End Agent'''

        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
                    Bạn là trợ lý thông minh chuyên về lũ lụt tại Việt Nam. Hãy dựa vào thông tin sau để trả lời câu hỏi:

                    Thông tin:
                    {context}

                    Câu hỏi:
                    {question}

                    Trả lời bằng tiếng Việt:
                    """,
                    )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=False,
            chain_type="stuff",
            chain_type_kwargs={"prompt": custom_prompt},
        )

    def run(self, query: str):
        try:  
            async def generate_response():
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(
                    ThreadPoolExecutor(),
                    functools.partial(self.qa_chain.invoke, {"query": query})
                )
                answer = response["result"] 

                for char in answer:
                    yield char
                    await asyncio.sleep(0.0002) 
            return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")


        except Exception as e:
            logging.error(f"Server error: {e}")
            return "An error occurred on the server."
        


    # def run(self, query: str):
    #     try:
    #         user_message = query

    #         async def generate_response():
    #             loop = asyncio.get_running_loop()
    #             response = await loop.run_in_executor(
    #                 ThreadPoolExecutor(),
    #                 functools.partial(self.executor.invoke, {"input": user_message})
    #             )
    #             answer = response.get("output")

    #             for char in answer:
    #                 yield char
    #                 await asyncio.sleep(0.0002) 
    #         return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")

    #     except Exception as e:
    #         logging.error(f"Server error: {e}")
    #         return "An error occurred on the server."
   