"""API v1 Router Aggregator."""

from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.root import router as root_router

api_v1_router = APIRouter()
api_v1_router.include_router(root_router)
api_v1_router.include_router(health_router)

__all__ = ["api_v1_router"]
