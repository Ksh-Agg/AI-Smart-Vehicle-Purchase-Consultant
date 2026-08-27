"""FastAPI lifespan context manager module."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.agentic import build_graph
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.session import SessionLocal

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

    async with AsyncPostgresSaver.from_conn_string(
        settings.checkpoint_database_url
    ) as checkpointer:
        graph, sql_agent_engine = build_graph(checkpointer, SessionLocal, settings)
        app.state.graph = graph
        app.state.checkpointer = checkpointer
        try:
            yield
        finally:
            sql_agent_engine.dispose()
            logger.info("Shutting down %s cleanly.", settings.PROJECT_NAME)
