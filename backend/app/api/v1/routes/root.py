"""Root welcome endpoint module."""

from fastapi import APIRouter

from app.api.dependencies.providers import SettingsDep
from app.schemas.root import RootResponse

router = APIRouter(tags=["Root"])


@router.get("/", response_model=RootResponse)
async def root(settings: SettingsDep) -> RootResponse:
    """Root endpoint returning welcome message, version, and running status."""
    return RootResponse(
        message=f"Welcome to {settings.PROJECT_NAME} API",
        version=settings.API_VERSION,
        status="running",
    )
