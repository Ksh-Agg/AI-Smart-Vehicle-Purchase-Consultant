"""ETL Logging Utility."""

import logging
import sys
from pathlib import Path

from app.etl.config import etl_settings


def configure_logger(source_name: str) -> logging.Logger:
    """Configures and returns a logger for a specific ETL source.

    Logs to both console and a log file in the logs directory.
    """
    logger = logging.getLogger(f"etl.{source_name}")
    logger.setLevel(etl_settings.LOG_LEVEL)

    # Prevent duplicating handlers if they already exist
    if logger.handlers:
        return logger

    # Formatter for structured/clear logs
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_dir = Path(etl_settings.LOGS_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_dir / f"etl_{source_name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
