from langchain.chat_models import init_chat_model
# data/db.py
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()
# read once at import time
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("put api key")



model = init_chat_model(model="gpt-4.1" , model_provider="openai", temperature=0.1, max_tokens=2000, api_key=api_key)

# reasoning_model = init_chat_model(model="o3", model_provider="openai", temperature=0.1, max_tokens=1000)