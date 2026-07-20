"""Health check endpoints module for API v1."""

from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint returning system status."""
    return {"status": "healthy"}
