from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(model: str = None, temperature: float = 0.0):
    selected_model = model or os.getenv("GROQ_MODEL") or "openai/gpt-oss-120b"
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(
        model=selected_model,
        temperature=temperature,
        api_key=api_key, 
    )