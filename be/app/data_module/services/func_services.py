from ..database.db import UserService

user_service_db = UserService("storage/users.db")
user_service_db.create_table()

def handle_User_Signup(username: str, email: str, phone: str, address: str):
    result = user_service_db.handle_user_signup(username=username, email=email, phone=phone, address=address)
    return result




  