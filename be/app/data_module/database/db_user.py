import sqlite3
import os

class UserService:
    def __init__(self, db_path: str):
        abs_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)  # Tạo thư mục nếu chưa có
        self.conn = sqlite3.connect(db_path, check_same_thread=False)  # Cho phép dùng trong FastAPI
        self.cursor = self.conn.cursor()
        self._create_table()

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

    def __del__(self):
        self.conn.close()
