"""FastAPI Main Application Entrypoint."""

from typing import Dict

from fastapi import FastAPI

from app.api.v1.routes import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    """Application factory initializing and configuring the FastAPI instance."""
    setup_logging()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )

    # Register API Routers
    application.include_router(api_v1_router, prefix="/api/v1")

    @application.get("/", response_model=Dict[str, str])
    async def root() -> Dict[str, str]:
        """Root endpoint returning welcome message."""
        return {
            "message": f"Welcome to {settings.PROJECT_NAME} API",
            "version": settings.API_VERSION,
        }

    return application


app = create_app()
