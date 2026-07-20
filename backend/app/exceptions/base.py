"""Base application exception class."""

from typing import Any


class ApplicationException(Exception):
    """Base class for all domain and application exceptions."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        details: Any = None,
        status_code: int = 500,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details
        self.status_code = status_code
