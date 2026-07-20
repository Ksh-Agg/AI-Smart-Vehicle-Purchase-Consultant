"""Dependency injection providers module.

This module will eventually provide FastAPI dependencies for:
- Settings & configuration (`get_settings`)
- Repositories & dataset access
- Feature preprocessing services
- Multi-model AI provider clients
- Recommendation engine orchestrators
- Authentication & authorization services
"""

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, settings


def get_settings() -> Settings:
    """Provide the application settings instance."""
    return settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
