import json
import os

def load_flood_data_local():
    # Đường dẫn tuyệt đối tới thư mục chứa file hiện tại (Utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Di chuyển lên 1 cấp rồi vào thư mục ChatBot/data
    file_path = os.path.abspath(os.path.join(current_dir, "..", "data", "responses.json"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {file_path}. Please ensure responses.json exists in ChatBot/data directory.")


def get_path_pdf_data(name: str):
    # Đường dẫn tuyệt đối tới thư mục chứa file hiện tại (Utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Di chuyển lên 1 cấp rồi vào thư mục ChatBot/data
    file_path = os.path.abspath(os.path.join(current_dir, "..", "data", name))

    try:
        return file_path
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {file_path}. Please ensure responses.json exists in ChatBot/data directory.")