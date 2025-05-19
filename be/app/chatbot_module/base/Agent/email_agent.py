from .tools import generate_email_tool, send_email_tool, get_user, get_current_datetime

class EmailAgent:
    def __init__(self):
        self.tools = [generate_email_tool, send_email_tool]
        self.tool_names = [tool.name for tool in self.tools]
        
    def run_email_agent(self):
        """Xử lý yêu cầu người dùng và quyết định lộ trình hành động"""
        list_user = get_user()
        date_time = get_current_datetime()
        
        for user in list_user:
            user_name = user["username"]
            email = user["email"]
            address = user["address"]
            email_content = generate_email_tool.invoke(
                {"username": user_name, 
                 "address": address, 
                 "date" : date_time
                 }).content
            recipient = email
            if not recipient:
                return f"Email đã được tạo nhưng không tìm thấy địa chỉ email người nhận:\n\n{email_content}\n\nVui lòng cung cấp địa chỉ email để gửi."
            # Gửi email đã tạo
            send_email_tool.invoke({
                "body": email_content,
                "to_email": recipient
            })
            print("Email đã được tạo và gửi đến {}".format(recipient))
        return "Tôi đã gửi cảnh báo đến tất cả người dùng có email được đăng ký !"
        
    



# from langchain_core.tools import BaseTool
# from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
# from langchain_community.chat_models import ChatOllama
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain.tools.render import format_tool_to_openai_function
# from langchain.agents.format_scratchpad import format_to_openai_functions
# from langchain_core.messages import AIMessage, HumanMessage
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from typing import List, Dict, Any
# from tools import generate_email_tool, send_email_tool
# import re

# class EmailAgent:
#     def __init__(self):
#         # Sử dụng ChatOllama thay vì load_model_Llama3
#         self.llm = ChatOllama(model="llama3", temperature=0.1)
        
#         # Định nghĩa các tools cho agent
#         self.tools = [generate_email_tool, send_email_tool]
        
#         # Chuẩn bị thông tin về tools để đưa vào prompt
#         tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
#         tool_names = ", ".join([tool.name for tool in self.tools])
        
#         # Tạo prompt cho agent với biến tools và tool_names
#         self.prompt = ChatPromptTemplate.from_messages([
#             ("system", """Bạn là một trợ lý AI chuyên nghiệp, giúp viết và gửi email.

#             Nhiệm vụ của bạn là giúp người dùng:
#             1. Viết email dựa trên yêu cầu của họ
#             2. Gửi email đến địa chỉ họ chỉ định

#             Các công cụ có sẵn:
#             {tools}

#             Tên các công cụ: {tool_names}

#             Hãy cẩn thận và xử lý mọi yêu cầu từng bước:
#             - Nếu người dùng muốn cả viết và gửi email, hãy thực hiện lần lượt cả hai bước
#             """),
#                         ("human", "{input}"),
#                         ("ai", "{agent_scratchpad}"),
#                     ])
        

#         self.agent = create_react_agent(
#             llm=self.llm,
#             tools=self.tools,
#             prompt=self.prompt
#         )

#         # Tạo agent executor
#         self.agent_executor = AgentExecutor(
#             agent=self.agent,
#             tools=self.tools,
#             verbose=True,
#             handle_parsing_errors=True,
#         )
        
#     def _extract_email_address(self, text):
#         """Trích xuất địa chỉ email từ văn bản"""
#         email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
#         match = re.search(email_pattern, text)
#         return match.group(0) if match else None
    
#     def run(self, user_input):
#         """Chạy agent để xử lý yêu cầu của người dùng"""
#         # Kiểm tra xem yêu cầu có liên quan đến email và có địa chỉ email không
#         has_email_addr = self._extract_email_address(user_input)
        
#         # Thêm gợi ý nếu yêu cầu không rõ ràng
#         if not has_email_addr and ("gửi" in user_input.lower() or "send" in user_input.lower()):
#             user_input += "\n(Vui lòng trước tiên viết email, sau đó yêu cầu tôi cung cấp địa chỉ email để gửi)"
            
#         try:
#             # Chuẩn bị dữ liệu đầu vào cho agent
#             tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
#             tool_names = ", ".join([tool.name for tool in self.tools])
            
#             # Thực thi agent
#             result = self.agent_executor.invoke({
#                 "input": user_input,
#                 "tools": tool_strings,
#                 "tool_names": tool_names
#             })
#             return result["output"]
#         except Exception as e:
#             # Xử lý trường hợp lỗi - fallback sang logic đơn giản
#             try:
#                 email_content = generate_email_tool.invoke(user_input)
#                 recipient = self._extract_email_address(user_input)
                
#                 if not recipient:
#                     return f"Email đã được tạo nhưng không tìm thấy địa chỉ email người nhận:\n\n{email_content}\n\nVui lòng cung cấp địa chỉ email để gửi."
                
#                 # Gửi email đã tạo
#                 send_params = {"body": email_content, "to_email": recipient}
#                 send_result = send_email_tool.invoke(send_params)
                
#                 return f"Email đã được tạo và gửi đến {recipient}:\n\n{email_content}\n\n{send_result}"
#             except Exception as e2:
#                 return f"Đã xảy ra lỗi khi xử lý yêu cầu: {str(e)}\n\nVui lòng cung cấp yêu cầu rõ ràng hơn về việc viết hoặc gửi email."

# # Cách sử dụng agent
# if __name__ == "__main__":
#     agent = EmailAgent()
    
#     # Ví dụ sử dụng
#     test_cases = [
#         "Viết và gửi email cảnh báo lũ lụt tại Quảng Nam cho địa chỉ emsimv22@gmail.com"
#     ]
    
#     for i, test in enumerate(test_cases):
#         print(f"\n--- Test case {i+1} ---")
#         print(f"Input: {test}")
#         print(f"Output: {agent.run(test)}")