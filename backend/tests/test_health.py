"""Isolated test suite for GET /api/v1/health endpoint."""

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_health_endpoint_success(client: TestClient) -> None:
    """Test health check endpoint status code and payload."""
    response = client.get(f"{settings.API_PREFIX}/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
