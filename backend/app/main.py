"""FastAPI Main Application Entrypoint."""

from fastapi import FastAPI

from app.api.v1.routes import api_v1_router
from app.core.config import settings
from app.exceptions.handlers import register_exception_handlers
from app.lifecycle.lifespan import lifespan
from app.middleware.registration import register_middleware


def create_app() -> FastAPI:
    """Application factory initializing and assembling the FastAPI application instance."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        description="AI-powered Smart Vehicle Purchase Consultant Backend API",
        summary="Intelligent vehicle evaluation and personalized recommendation API.",
        debug=settings.DEBUG,
        lifespan=lifespan,
        contact={
            "name": "SVPC Development Team",
        },
        license_info={
            "name": "MIT",
        },
    )

    # Register Middleware
    register_middleware(application)

    # Register Exception Handlers
    register_exception_handlers(application)

    # Register API Routers
    application.include_router(api_v1_router, prefix=settings.API_PREFIX)

    return application


app = create_app()
