import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.main import app

Faker.seed(42)


@pytest.fixture(scope="session")
def base_client():
    """Base test client for the application"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_db():
    """Mock database session"""
    session = MagicMock(spec=Session)
    session.query = MagicMock()
    session.add = MagicMock()
    session.flush = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.refresh = MagicMock()
    session.close = MagicMock()
    return session
