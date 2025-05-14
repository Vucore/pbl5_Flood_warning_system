from ..Utils.get_path_file import load_json_local_data
from underthesea import word_tokenize
import string
import re

def preprocess_text(text: str) -> str:
    text = __normalize_whitespace(text=text)
    text = __normalize_contractions(text=text)
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())  
    text = word_tokenize(text, format="text") 
    return text

def __normalize_contractions(text: str):
    contraction_list = load_json_local_data("vietnamese_contractions.json")
    norm_text = __normalize_contractions_text(text, contraction_list)
    
    return norm_text

def __normalize_contractions_text(text, contractions):
    """
    Hàm này chuẩn hóa các từ viết tắt trong văn bản.
    """
    new_token_list = []
    token_list = text.split()
    for word_pos in range(len(token_list)):
        word = token_list[word_pos]
        first_upper = False
        # Kiểm tra xem từ có chữ cái đầu là chữ hoa không
        if word[0].isupper():
            first_upper = True
        # Nếu từ có trong danh sách từ viết tắt
        if word.lower() in contractions:
            replacement = contractions[word.lower()]
            if first_upper:
                replacement = replacement[0].upper() + replacement[1:]
            replacement_tokens = replacement.split()  # Tách các từ thay thế
            print(replacement_tokens)
            # Nếu thay thế có nhiều từ
            if len(replacement_tokens) > 1:
                new_token_list.append(replacement_tokens[0])
                new_token_list.append(replacement_tokens[1])
            else:
                new_token_list.append(replacement_tokens[0])
        else:
            new_token_list.append(word)
    sentence = " ".join(new_token_list).strip(" ")
    return sentence

def __normalize_whitespace(text: str):
    """
    Hàm này chuẩn hóa khoảng trắng, loại bỏ các khoảng trắng dư thừa.
    """
    corrected = str(text)
    corrected = re.sub(r"//t", r"\t", corrected)
    corrected = re.sub(r"( )\1+", r"\1", corrected)
    corrected = re.sub(r"(\n)\1+", r"\1", corrected)
    corrected = re.sub(r"(\r)\1+", r"\1", corrected)
    corrected = re.sub(r"(\t)\1+", r"\1", corrected)
    return corrected.strip(" ")
