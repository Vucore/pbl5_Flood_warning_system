from ..database.db import UserService
from fastapi import HTTPException
import random
from io import StringIO
import os
import csv
import re

user_service_db = UserService("storage/users.db")
user_service_db.create_table_users()

# Sử dụng đường dẫn tuyệt đối
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOG_DIR = os.path.join(BASE_DIR, "conversation_logs")

async def handle_user_signup(username: str, email: str, phone: str, address: str):
    result = await user_service_db.handle_user_signup(username=username, email=email, phone=phone, address=address)
    return result

def handle_login(email: str):
    result = user_service_db.check_user_exists(email=email)
    return {"success": result, "id": random.randint(0, 1000)}

def admin_auth(password: str):
    if password == user_service_db.get_admin_password():
        return {"success": True, "message": "Đăng nhập thành công"}
    else:
        return {"success": False, "message": "Mật khẩu không đúng"}

def update_pass_admin(password: str):
    user_service_db.update_admin_password(password)

def update_user_status_sqlite(email: str, isOnline: bool, lastLogin: int):
    result = user_service_db.update_user_status_sqlite(email, isOnline, lastLogin)
    return result

def get_list_user():
    result = user_service_db.get_all_users()
    return result 

def get_chat_history():
    try:
        if not os.path.exists(LOG_DIR):
            print(f"Log directory not found at: {LOG_DIR}")
            raise HTTPException(status_code=404, detail="Log directory not found")

        # Tìm tất cả file CSV khớp với mẫu conversation_log_YYYY-MM-DD.csv
        csv_files = [
            f for f in os.listdir(LOG_DIR)
            if re.match(r'conversation_log_\d{4}-\d{2}-\d{2}\.csv$', f)
        ]
        # print(f"Found CSV files: {csv_files}")

        if not csv_files:
            print(f"No CSV files found in: {LOG_DIR}")
            raise HTTPException(status_code=404, detail="No chat history files found")

        # Chuẩn bị buffer để hợp nhất dữ liệu CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Viết header cho CSV đầu ra
        header = ["timestamp", "question", "answer", "rag_used", "rag_documents", "response_type"]
        writer.writerow(header)

        # Đọc và hợp nhất dữ liệu từ tất cả file CSV
        for csv_file in sorted(csv_files, reverse=True):  # Sắp xếp file theo thứ tự mới nhất
            file_path = os.path.join(LOG_DIR, csv_file)
            try:
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Bỏ qua header của mỗi file
                    for row in reader:
                        if row:  
                            writer.writerow(row)
                            # print(f"Writing row: {row}")
            except Exception as e:
                print(f"Error reading file {csv_file}: {str(e)}")
                continue

        result = output.getvalue()
        # print(f"Final CSV output: {result[:200]}...")  # Print first 200 chars
        return result
    except Exception as e:
        print(f"Error in get_chat_history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving CSV files: {str(e)}")