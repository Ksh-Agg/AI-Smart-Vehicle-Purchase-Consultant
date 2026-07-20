"""FastAPI lifespan context manager module."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifespan events."""
    # Startup handlers
    setup_logging()
    logger.info(
        "Starting %s v%s (Environment: %s, Log Level: %s)",
        settings.PROJECT_NAME,
        settings.API_VERSION,
        settings.ENVIRONMENT.value,
        settings.LOG_LEVEL.value,
    )

    yield

    # Shutdown handlers
    logger.info("Shutting down %s cleanly.", settings.PROJECT_NAME)
