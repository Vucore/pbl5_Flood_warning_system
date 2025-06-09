from ..database.db import UserService
import random
user_service_db = UserService("storage/users.db")
user_service_db.create_table_users()


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