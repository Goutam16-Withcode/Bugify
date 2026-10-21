from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(model: str = None, temperature: float = 0.0):
    selected_model = model or os.getenv("GROQ_MODEL") or "qwen/qwen3.8-27b"
    api_key = os.getenv("GROQ_API_KEY")
    
    primary = ChatGroq(
        model=selected_model,
        temperature=temperature,
        api_key=api_key,
        max_retries=1,
    )
    
    fallbacks = []
    for fb in ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]:
        if fb != selected_model:
            fallbacks.append(ChatGroq(model=fb, temperature=temperature, api_key=api_key, max_retries=1))
            
    return primary.with_fallbacks(fallbacks) if fallbacks else primary