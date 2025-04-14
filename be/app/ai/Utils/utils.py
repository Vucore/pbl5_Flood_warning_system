import string
from underthesea import word_tokenize

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    text = word_tokenize(text, format="text")
    return text
