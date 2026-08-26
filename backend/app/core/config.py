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

    # AI Service Configuration
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=(REPOSITORY_DIR / ".env", BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
