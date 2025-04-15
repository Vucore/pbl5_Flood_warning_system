from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from ..ML.embedding import VietnameseRetrieverBuilder
import asyncio
import functools
import logging
class Agent():
    def __init__(self, llm):
        self.retrieverBuilder = VietnameseRetrieverBuilder()
        self.retriever = self.retrieverBuilder.build()
        self.llm = llm
        self.retriever_tool = create_retriever_tool(
            self.retriever,  
            "find_documents",
            "Search for information."
        )

        self.tools = [self.retriever_tool]

        # Tạo prompt template
        self.system_prompt = """Bạn là một trợ lý thông minh.
        Dưới đây là các đoạn văn bản được trích xuất từ tài liệu. Dựa vào tài liệu đó hãy trả lời câu hỏi của tôi.'
        Luôn trả lời bằng tiếng Việt."""


        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Tạo agent từ LLM, prompt và tools
        self.agent = create_openai_functions_agent(llm=llm, tools=self.tools, prompt=self.prompt)

        # Tạo agent executor để sử dụng
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    
    def run(self, query: str):
        try:
            user_message = query

            async def generate():
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(
                    ThreadPoolExecutor(),
                    functools.partial(self.executor.invoke, {"input": user_message})
                )
                answer = response.get("output")

                for char in answer:
                    yield char
                    await asyncio.sleep(0.002)

            return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")

        except Exception as e:
            logging.error(f"Server error: {e}")
            return "An error occurred on the server."

