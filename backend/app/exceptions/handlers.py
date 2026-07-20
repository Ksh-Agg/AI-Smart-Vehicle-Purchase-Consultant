"""Global FastAPI exception handlers."""

from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.exceptions.base import ApplicationException

logger = get_logger(__name__)


def _format_error_response(
    code: str, message: str, details: Any = None
) -> Dict[str, Any]:
    """Format standardized error response dictionary."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


async def application_exception_handler(
    request: Request, exc: ApplicationException
) -> JSONResponse:
    """Handle custom ApplicationException instances."""
    logger.error("Application error [%s]: %s", exc.code, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=_format_error_response(exc.code, exc.message, exc.details),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle FastAPI request validation errors."""
    logger.warning("Request validation error: %s", exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_format_error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details=exc.errors(),
        ),
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle uncaught exceptions as internal server errors."""
    logger.critical("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_format_error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal server error occurred.",
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers with the FastAPI application."""
    app.add_exception_handler(ApplicationException, application_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
