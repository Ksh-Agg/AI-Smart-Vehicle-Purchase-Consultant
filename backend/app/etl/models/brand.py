"""Canonical Brand Pydantic Model."""

from pydantic import BaseModel, Field


class CanonicalBrand(BaseModel):
    """Canonical model for Brand data matching the database schema."""

    name: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    origin: str | None = Field(None, max_length=100)

    class Config:
        frozen = True
