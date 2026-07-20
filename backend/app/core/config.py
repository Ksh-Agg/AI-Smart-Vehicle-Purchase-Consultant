"""Application configuration module using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings class loading environment variables."""

    PROJECT_NAME: str = "Smart Vehicle Purchase Consultant"
    API_VERSION: str = "v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # AI Service Configuration
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
