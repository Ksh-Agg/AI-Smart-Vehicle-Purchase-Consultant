"""Isolated test suite for GET /api/v1/ root endpoint."""

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_root_endpoint_success(client: TestClient) -> None:
    """Test successful root endpoint response payload and status code."""
    response = client.get(settings.API_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == f"Welcome to {settings.PROJECT_NAME} API"
    assert data["version"] == settings.API_VERSION
    assert data["status"] == "running"
