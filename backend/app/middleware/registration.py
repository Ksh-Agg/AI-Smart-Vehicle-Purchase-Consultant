"""Middleware registration helper module."""

from fastapi import FastAPI

from app.core.logging import get_logger

logger = get_logger(__name__)


def register_middleware(app: FastAPI) -> None:
    """Register ASGI middleware with the FastAPI application.

    Future middleware registration (CORS, GZip, TrustedHost, HTTPS Redirect, Rate Limiting)
    will be added here once networking & origin policies are finalized.
    """
    logger.debug("Middleware registration hook initialized.")
