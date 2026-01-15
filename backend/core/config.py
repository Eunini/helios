"""Configuration management for Helios backend."""

import os
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_TITLE: str = "Helios API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./helios.db"
    DATABASE_ECHO: bool = False

    # LLM Configuration
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2048

    # Vector Store Configuration
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "helios_business_memory"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Security
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    API_KEY_HEADER: str = "X-API-Key"

    # Feature Flags
    ENABLE_WEBSOCKETS: bool = True
    ENABLE_VECTOR_STORE: bool = True
    MAX_TASK_QUEUE_SIZE: int = 100

    # Voice & Video Configuration
    OPENAI_API_KEY: Optional[str] = None
    VIDEO_CHAT_ENABLED: bool = True
    VOICE_VIDEO_LOG_LEVEL: str = "INFO"
    ENABLE_VOICE_VIDEO_DEBUG: bool = False
    VOICE_RATE_LIMIT_PER_MINUTE: int = 60
    VOICE_RATE_LIMIT_PER_HOUR: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra environment variables


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
