from langchain.prompts import PromptTemplate
from fastapi.responses import StreamingResponse
from ..RAG.file_loader import DocumentLoader
from ..RAG.setup_spilitter import TextSplitter
from ..RAG.vectorstore import VectorDB
from ..RAG.setup_retriever import Retriever
from ..Utils.conversation_logger import ConversationLogger
import asyncio

class RAGAgent():
    def __init__(self, llm, embedding):
        self.llm = llm
        self.embedding = embedding
        self.document_loader = DocumentLoader()
        self.splitter_class = TextSplitter()
        self.vectorstore = None
        self.retriever_class = Retriever()
        self.retriever = None
        self.ensemble_retriever = None
        self.conversation_logger = ConversationLogger()
        self.process_documents()
        self.build_ensemble_retriever()

    def process_documents(self):
        # documents = self.pdf_loader.load_pdf_docs()
        documents = self.document_loader.load_markdown_docs()
        docs = self.splitter_class.split_documents(documents=documents)
        self.vectorstore = VectorDB(docs=docs,
                                          embedding=self.embedding
                                        ).get_vectorstore()
        self.retriever = self.retriever_class.build_retriever(docs=docs, k=3)

    def build_ensemble_retriever(self):
        self.ensemble_retriever = self.retriever_class.get_ensemble_retriever(vectorstore=self.vectorstore, retriever=self.retriever)

        self.custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
                    Bạn là một trợ lý AI chuyên về cảnh báo lũ lụt, mực nước và lượng mưa hoặc các chỉ số thời tiết được cung cấp tài liệu.
                    Chỉ dựa vào thông tin tìm được từ công cụ và kiến thức nội tại của bạn về chủ đề này để trả lời.
                    Nếu không tìm thấy thông tin trong tài liệu, hãy nói rằng bạn không có thông tin đó trong tài liệu được cung cấp.
                    Luôn trả lời bằng tiếng Việt một cách rõ ràng và chi tiết nhất có thể dựa trên thông tin có được, không thêm bất kỳ văn bản nào khác.
                    
                    Thông tin:
                    {context}

                    Câu hỏi:
                    {question}
                    Hãy trả lời bằng tiếng Việt!
                    """,
                    )

    def run_rag(self, query: str):
        async def stream_answer(llm, prompt: str):
            for chunk in llm.stream(prompt):
                if hasattr(chunk, "content"):
                    for token in chunk.content:
                        yield token
                        await asyncio.sleep(0.002)

        async def generate_response():
            '''Retrieval'''
            docs = self.ensemble_retriever.invoke(query)  
            # In thông tin chi tiết về từng document
            print("\n=== Retrieved Documents ===")
            for i, doc in enumerate(docs, 1):
                print(f"\nDocument {i}:")
                print(f"Content: {doc.page_content}")
                print(f"Metadata: {doc.metadata}")
            print("=" * 50)

            '''Context'''
            context = "\n".join([doc.page_content for doc in docs])
            max_context_length = 10000  
            if len(context) > max_context_length:
                context = context[:max_context_length]

            '''Prompt'''
            prompt = self.custom_prompt.format(context=context, question=query)

            response_text = ""
            async for token in stream_answer(self.llm, prompt):
                response_text += token
                yield token

            # Log the conversation after response is complete
            self.conversation_logger.log_conversation(
                question=query,
                answer=response_text,
                rag_used=True,
                rag_documents=docs,
                response_type="simple"
            )

        return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")

    def run_llm(self, query: str):
        async def stream_answer(llm, prompt: str):
            for chunk in llm.stream(prompt):
                if hasattr(chunk, "content"):
                    for token in chunk.content:
                        yield token
                        await asyncio.sleep(0.002)
        prompt = "Hãy trả lời bằng tiếng Việt cho câu hỏi {}".format(query)
        
        async def generate_response():
            response_text = ""
            async for token in stream_answer(self.llm, prompt):
                response_text += token
                yield token

            # Log the conversation after response is complete
            self.conversation_logger.log_conversation(
                question=query,
                answer=response_text,
                rag_used=False,
                response_type="chat"
            )

        return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")
    

        # self.qa_chain = RetrievalQA.from_chain_type(
    #     llm=self.llm,
    #     retriever=self.retriever,
    #     return_source_documents=False,
    #     chain_type="stuff",
    #     chain_type_kwargs={"prompt": self.custom_prompt},
    # )


    # def run(self, query: str):
    #     try:  
    #         async def generate_response():
    #             loop = asyncio.get_running_loop()
    #             response = await loop.run_in_executor(
    #                 ThreadPoolExecutor(),
    #                 functools.partial(self.qa_chain.invoke, {"query": query})
    #             )
    #             answer = response["result"] 

    #             for char in answer:
    #                 yield char
    #                 await asyncio.sleep(0.0002) 
    #         return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")


    #     except Exception as e:
    #         logging.error(f"Server error: {e}")
    #         return "An error occurred on the server."


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