"""ETL module configuration."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base data directory is SVPC/backend/data
BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = BASE_DIR / "data"


class ETLSettings(BaseSettings):
    """ETL-specific settings class."""

    RAW_DIR: Path = DEFAULT_DATA_DIR / "raw"
    STAGING_DIR: Path = DEFAULT_DATA_DIR / "staging"
    PROCESSED_DIR: Path = DEFAULT_DATA_DIR / "processed"
    REJECTED_DIR: Path = DEFAULT_DATA_DIR / "rejected"
    MASTER_DIR: Path = DEFAULT_DATA_DIR / "master"
    LOGS_DIR: Path = DEFAULT_DATA_DIR / "logs"

    BATCH_SIZE: int = 100
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="ETL_",
        extra="ignore",
    )


etl_settings = ETLSettings()
