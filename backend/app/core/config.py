"""Application configuration module using Pydantic Settings."""

from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
REPOSITORY_DIR = BASE_DIR.parent


class Environment(str, Enum):
    """Execution environment enumeration."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging level enumeration."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """Central application settings class loading environment variables."""

    PROJECT_NAME: str = "Smart Vehicle Purchase Consultant"
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: LogLevel = LogLevel.INFO
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Database Configuration
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "svpc"
    DATABASE_USER: str = "svpc"
    DATABASE_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    @property
    def database_dsn(self) -> str:
        """Psycopg-compatible DSN used by LangGraph persistence."""
        return self.database_url.replace("postgresql+psycopg://", "postgresql://", 1)

    # AI Service Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_CHAT_MODEL: str = "gemini-3.7-flash"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"
    AGENT_TOP_K_PRELIMINARY: int = 5
    AGENT_TOP_K_FINAL: int = 3
    AGENT_TIMEOUT_SECONDS: int = 120
    CATALOGUE_STATEMENT_TIMEOUT_MS: int = 8_000
    RAG_COLLECTION_NAME: str = "maruti_official_documents"
    CATALOGUE_AGENT_DATABASE_URL: str = ""
    CHECKPOINT_DATABASE_URL: str = ""
    ALLOWED_RESEARCH_DOMAINS: str = (
        "marutisuzuki.com,marutisuzukitruevalue.com,bncap.in"
    )

    @property
    def catalogue_agent_database_url(self) -> str:
        return self.CATALOGUE_AGENT_DATABASE_URL or self.database_url

    @property
    def checkpoint_database_url(self) -> str:
        return self.CHECKPOINT_DATABASE_URL or self.database_dsn

    @property
    def allowed_research_domains(self) -> tuple[str, ...]:
        return tuple(
            domain.strip().lower()
            for domain in self.ALLOWED_RESEARCH_DOMAINS.split(",")
            if domain.strip()
        )

    model_config = SettingsConfigDict(
        env_file=REPOSITORY_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
