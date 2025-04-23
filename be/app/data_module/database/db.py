import sqlite3
import os
from typing import Optional

class UserService:
    def __init__(self, db_path: Optional[str] = None):
        self.conn = None
        self.cursor = None

        if db_path:
            abs_path = os.path.abspath(db_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)  # Tạo thư mục nếu chưa có
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            # self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT
            )
        """)
        self.conn.commit()

    def handle_user_signup(self, username: str, email: str, phone: str, address: str):
        try:
            self.cursor.execute("""
                INSERT INTO users (username, email, phone, address)
                VALUES (?, ?, ?, ?)
            """, (username, email, phone, address))
            self.conn.commit()

            return {
                "success": True,
                "message": "Đăng ký thành công"
            }

        except Exception as e:
            print("Lỗi khi lưu vào database:", e)
            return {
                "success": False,
                "message": "Đăng ký thất bại",
                "error": str(e)
            }
        
    def get_all_users(self):
        try:
            self.cursor.execute("""
                SELECT * FROM users
            """)
            users = self.cursor.fetchall()  # Lấy tất cả dữ liệu người dùng

            user_list = []
            for user in users:
                user_list.append({
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "phone": user[3],
                    "address": user[4]
                })

            return {
                "success": True,
                "users": user_list
            }

        except Exception as e:
            print("Lỗi khi truy vấn database:", e)
            return {
                "success": False,
                "message": "Không thể lấy danh sách người dùng",
                "error": str(e)
            }
        
    def __del__(self):
        self.conn.close()

def get_all_users_from_db(db_path: str):
    try:
        abs_path = os.path.abspath(db_path)
        conn = sqlite3.connect(abs_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
        """)
        users = cursor.fetchall()

        conn.close()

        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "phone": user[3],
                "address": user[4]
            })

        return {
            "success": True,
            "users": user_list
        }

    except Exception as e:
        print("Lỗi khi truy vấn database:", e)
        return {
            "success": False,
            "message": "Không thể lấy danh sách người dùng",
            "error": str(e)
        }


# class ChatbotService():
#     def __init__(self, db_path: str):
#         abs_path = os.path.abspath(db_path)
#         os.makedirs(os.path.dirname(abs_path), exist_ok=True)  # Tạo thư mục nếu chưa có
#         self.conn = sqlite3.connect(db_path, check_same_thread=False)  # Cho phép dùng trong FastAPI
#         self.cursor = self.conn.cursor()
#         self._create_tables()
#     def _create_tables(self):
#         # Tạo bảng patterns nếu chưa có
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS patterns (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 pattern TEXT NOT NULL,
#                 embedding BLOB NOT NULL
#             )
#         """)

#         self.conn.commit()
#     def save_pattern_and_embedding(self, pattern: str, embedding):
#         """
#         Lưu một pattern và embedding của nó vào cơ sở dữ liệu SQLite.
#         """
#         try:
#             # Lưu embedding dưới dạng nhị phân
#             embedding_blob = pickle.dumps(embedding)

#             self.cursor.execute("""
#                 INSERT INTO patterns (pattern, embedding)
#                 VALUES (?, ?)
#             """, (pattern, embedding_blob))
#             self.conn.commit()

#             return {
#                 "success": True,
#                 "message": "Pattern và embedding đã được lưu thành công"
#             }
        
#         except Exception as e:
#             print("Lỗi khi lưu pattern và embedding:", e)
#             return {
#                 "success": False,
#                 "message": "Lưu pattern và embedding thất bại",
#                 "error": str(e)
#             }

#     def __del__(self):
#         self.conn.close()

