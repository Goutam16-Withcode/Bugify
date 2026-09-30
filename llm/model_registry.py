import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()


_REGISTRY: dict[str, type] = {}


def _get_groq(model: str = "llama-3.3-70b-versatile", temperature: float = 0.0) -> BaseChatModel:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in environment / .env")
    return ChatGroq(model=model, temperature=temperature, api_key=api_key)


def _get_openai(model: str = "gpt-4o", temperature: float = 0.0) -> BaseChatModel:
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError("langchain-openai is required. Run: pip install langchain-openai")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set")
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


def _get_anthropic(model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.0) -> BaseChatModel:
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError:
        raise ImportError("langchain-anthropic is required. Run: pip install langchain-anthropic")
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set")
    return ChatAnthropic(model=model, temperature=temperature, api_key=api_key)


def get_model(
    provider: str = "groq",
    model: str | None = None,
    temperature: float = 0.0,
) -> BaseChatModel:
    """
    Factory function to build a chat model from a provider name.

    Supported providers: "groq", "openai", "anthropic"
    """
    provider = provider.lower().strip()

    defaults = {
        "groq": "llama-3.3-70b-versatile",
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-20241022",
    }

    model_name = model or defaults.get(provider, "llama-3.3-70b-versatile")

    if provider == "groq":
        return _get_groq(model_name, temperature)
    elif provider == "openai":
        return _get_openai(model_name, temperature)
    elif provider == "anthropic":
        return _get_anthropic(model_name, temperature)
    else:
        raise ValueError(f"Unknown LLM provider: {provider!r}. Choose from: groq, openai, anthropic")
