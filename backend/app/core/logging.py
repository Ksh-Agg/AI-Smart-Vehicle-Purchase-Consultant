"""Centralized logging configuration module."""

import logging
import sys

from app.core.config import settings


def setup_logging(log_level: str | None = None) -> None:
    """Establish reusable logging configuration."""
    level_str = log_level or settings.LOG_LEVEL.value
    level = getattr(logging, level_str.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Obtain a logger instance for the given module name."""
    return logging.getLogger(name)
