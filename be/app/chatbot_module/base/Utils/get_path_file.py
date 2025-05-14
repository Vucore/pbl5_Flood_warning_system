import json
import os
from typing import List

# Đường dẫn tuyệt đối
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")

def load_json_local_data(json_name: str):


    # Di chuyển lên 1 cấp rồi vào thư mục ChatBot/data
    file_path = os.path.abspath(os.path.join(current_dir, "..", "data", json_name))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {file_path}. Please ensure responses.json exists in ChatBot/data directory.")

    
def get_path_and_name_pdf_data() -> List[str]:
    pdf_paths = []
    pdf_names = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            pdf_names.append(filename)
            file_path = os.path.join(data_dir, filename)
            pdf_paths.append(os.path.abspath(file_path))
    return pdf_paths, pdf_names

def get_path_and_name_markdown_data() -> List[str]:
    markdown_paths = []
    markdown_names = []
    for filename in os.listdir(data_dir):
        if filename.endswith((".md", ".markdown")):
            markdown_names.append(filename)
            file_path = os.path.join(data_dir, filename)
            markdown_paths.append(os.path.abspath(file_path))
    return markdown_paths, markdown_names