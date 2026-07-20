"""Pytest fixtures configuration module."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI TestClient instance for testing routes."""
    with TestClient(app) as test_client:
        yield test_client
