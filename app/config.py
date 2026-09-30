import os
from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class LLMProvider(str, Enum):
    GROQ = "groq"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------------------------------------
    # Application
    # -------------------------------------------------------
    app_name: str = "Bugify"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    # -------------------------------------------------------
    # API server
    # -------------------------------------------------------
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["*"]

    # -------------------------------------------------------
    # LLM
    # -------------------------------------------------------
    llm_provider: LLMProvider = LLMProvider.GROQ
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    groq_model: str = "llama-3.3-70b-versatile"
    openai_model: str = "gpt-4o"
    llm_temperature: float = 0.0
    llm_max_retries: int = 3

    # -------------------------------------------------------
    # Orchestrator
    # -------------------------------------------------------
    max_iterations: int = 3

    # -------------------------------------------------------
    # Vector DB / RAG
    # -------------------------------------------------------
    qdrant_url: str = Field(default="", alias="QDRANT_URL")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")
    embedding_model: str = "all-MiniLM-L6-v2"

    # -------------------------------------------------------
    # Web Search
    # -------------------------------------------------------
    tavily_api_key: str = Field(default="", alias="TAVILY_API_KEY")

    # -------------------------------------------------------
    # LangSmith tracing
    # -------------------------------------------------------
    langchain_tracing_v2: bool = Field(default=False, alias="LANGCHAIN_TRACING_V2")
    langchain_api_key: str = Field(default="", alias="LANGCHAIN_API_KEY")
    langchain_project: str = Field(default="Bugify", alias="LANGCHAIN_PROJECT")

    # -------------------------------------------------------
    # Sandbox
    # -------------------------------------------------------
    sandbox_timeout: int = 60
    use_docker_sandbox: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
