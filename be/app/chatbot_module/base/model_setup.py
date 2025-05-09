from langchain_community.chat_models import ChatOllama
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
import os

load_dotenv() 

ENCODER_MODEL_NAME = os.getenv("ENCODER_MODEL_NAME")

MAX_TOKENS = 2048

def load_vietnamese_encoder_model():
    model_name = ENCODER_MODEL_NAME
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

def load_model_Llama3(temperature: float = 0.1):
    llm = ChatOllama(model="llama3", temperature=temperature, max_tokens=MAX_TOKENS) 
    return llm