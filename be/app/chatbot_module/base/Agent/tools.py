from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ....data_module.database.db import get_all_users_from_db
from ..model_setup import load_model_Llama3
from datetime import datetime
import smtplib

GMAIL_USER = 'emsimv10@gmail.com'
GMAIL_PASS = 'vrlinivaocehbnzh'      # ← App password từ Google

# Viết mail
def generate_email(username, address, date):
    llm = load_model_Llama3(temperature=0.1)
    prompt = PromptTemplate(
        input_variables=["username", "address", "date"],
        template=(
            "Bạn là một trợ lý AI. Bạn sẽ đại diện cho `Hệ thống gửi mail tự động` để viết email chuyên nghiệp bằng tiếng Việt\n"
            "Nội dung gmail là cảnh báo lũ lụt đến người nhận\n"
            "Thông tin người nhận:\n"
            "- Tên: {username}\n"
            "- Địa chỉ: {address}\n"
            "- Thời điểm hiện tại: {date}\n\n"
            "Hãy viết một email hoàn chỉnh, nội dung rõ ràng, giọng văn phù hợp bằng tiếng Việt chỉ trả về nội dung email mà bạn viết, không thêm bất kỳ văn bản nào khác.\n\n"
        )
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({
        "username": username,
        "address": address,
        "date" : date
    })

@tool
def generate_email_tool(username, address, date):
    """Viết email hoàn chỉnh dựa trên hướng dẫn người dùng."""
    email_body = generate_email(username, address, date)
    return email_body

# Gửi mail
def send_email(body, to_email):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)

            msg = MIMEMultipart()
            msg["From"] = GMAIL_USER
            msg["To"] = to_email
            msg["Subject"] = "📬Thư gửi từ hệ thống tự động cảnh báo lũ lụt"
            msg.attach(MIMEText(body, "plain"))

            server.send_message(msg)
            print(f"✅ Đã gửi email đến {to_email}")

    except Exception as e:
        print("❌ Gửi email thất bại:", str(e))


@tool
def send_email_tool(to_email: str, body: str) -> str:
    """Gửi email đến một hoặc nhiều địa chỉ với nội dung cụ thể."""
    send_email(body, to_email)


def get_user():
    result = get_all_users_from_db("storage/users.db")
    if result['success']:
        return [
            {
                "username": user["username"],
                "email": user["email"],
                "phone": user["phone"],
                "address": user["address"]
            }
            for user in result["users"]
        ]
    else:
        print("Lỗi khi lấy dữ liệu:", result["message"])
        return []


def adaptive_approach(query: str):
    # Prompt phân loại
    llm = load_model_Llama3(temperature=0.1)
    query_classifier_prompt = PromptTemplate.from_template("""
    Phân loại câu hỏi sau thành 1 trong 3 loại:
    - "chat" nếu là trò chuyện hoặc kiến thức phổ thông
    - "simple" nếu là câu hỏi liên quan đến vấn đề lũ lụt, thiên tai, giải pháp ứng phó, hậu quả của lũ lụt,.. cần truy xuất thông tin trong tài liệu
    - "call" nếu câu có ý nghĩa như muốn gửi cảnh báo, gửi email, gửi thư,... đến người dùng 

    Câu hỏi: {query}
    Loại câu hỏi (chỉ trả về: chat, simple, call):
    """)

    chain = RunnableSequence(
        query_classifier_prompt | llm | StrOutputParser()
    )
    return chain.invoke({
        "query": query,
    })

@tool
def query_classifier(query: str):
    """Phân loại câu hỏi người dùng"""
    question_type = adaptive_approach(query)
    return question_type

def get_current_datetime():
    """Lấy ngày và giờ hiện tại"""
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")