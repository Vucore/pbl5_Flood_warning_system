import sqlite3
import os
from typing import Optional
import datetime

class UserService:
    def __init__(self, db_path: Optional[str] = None):
        self.conn = None
        self.cursor = None

        if db_path:
            abs_path = os.path.abspath(db_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)  
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
        self.__create_table_admin()
        self.__create_admin_account("admin123")

    def __create_table_admin(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()
    def __create_admin_account(self, password: str):
        self.cursor.execute("SELECT COUNT(*) FROM admin")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            # Nếu chưa có, thì chèn tài khoản admin
            self.cursor.execute("""
                INSERT INTO admin (password)
                VALUES (?)
            """, (password,))
            self.conn.commit()
        else:
            print("Admin account already exists. Skipping creation.")

    def update_admin_password(self, new_password):
        self.cursor.execute("""
            UPDATE admin
            SET password = ?
        """, (new_password,))
        self.conn.commit()

    def get_admin_password(self):
        self.cursor.execute("""
            SELECT password FROM admin
        """)
        password = self.cursor.fetchone()[0]
        return password

    def create_table_users(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT,
                status TEXT,
                lastLogin DATETIME
            )
        """)
        self.conn.commit()

    async def handle_user_signup(self, username: str, email: str, phone: str, address: str):
        try:
            if self.check_user_exists(email=email):
                return {
                "success": False,
                "message": "Email đã được đăng ký",
            }

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
    def check_user_exists(self, email: str):
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM users WHERE email = ?
            """, (email,))
            
            count = self.cursor.fetchone()[0]
            if count > 0:
                return True
            else:
                return False

        except Exception as e:
            print("Lỗi khi kiểm tra email:", e)
            return {
                "success": False,
                "message": "Không thể kiểm tra email",
                "error": str(e)
            }
    def update_user_status_sqlite(self, email: str, isOnline: bool, lastLogin: int):
        try:
            # Kiểm tra xem user có tồn tại không
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone()[0] == 0:
                return {"success": False, "error": f"User with email {email} does not exist"}

            status = "online" if isOnline else "offline"
            last_login_dt = datetime.datetime.fromtimestamp(lastLogin / 1000).strftime("%Y-%m-%d %H:%M:%S")
            # print(f"Updating user status - email={email}, status={status}, last_login_dt={last_login_dt}")

            self.cursor.execute("""
                UPDATE users
                SET status = ?, 
                    lastLogin = ?
                WHERE email = ?
            """, (status, last_login_dt, email))

            if self.cursor.rowcount == 0:
                return {"success": False, "error": "No rows were updated"}

            self.conn.commit()

            return {"success": True, "status": status}
        except Exception as e:
            print(f"Error updating user status: {str(e)}")
            return {"success": False, "error": str(e)}
        
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
                    "address": user[4],
                    "status": user[5],
                    "lastLogin": user[6]
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