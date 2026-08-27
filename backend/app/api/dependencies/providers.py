"""Dependency injection providers module.

This module provides the small shared dependency set used by API routes.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, settings
from app.db.session import get_db


def get_settings() -> Settings:
    """Provide the application settings instance."""
    return settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[Session, Depends(get_db)]
