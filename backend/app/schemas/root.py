"""Root endpoint response schema."""

from pydantic import BaseModel


class RootResponse(BaseModel):
    """Response model for the root welcome endpoint."""

    message: str
    version: str
    status: str
