from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.auth.router import get_auth_service
from app.modules.auth.schemas import TokenResponse, VerifyTokenResponse
from tests.factories.user_factory import UserFactory


@pytest.fixture
def mock_auth_service():
    """Mock auth service"""
    return MagicMock()


@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)


class TestRegister:
    """Test register endpoint"""
    
    def test__register__valid_data__creates_user(self, client, mock_auth_service):
        # Arrange
        user = UserFactory.build()
        mock_auth_service.register_user.execute.return_value = user
        
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        payload = {"username": "testuser", "email": "test@example.com", "password": "password123"}
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["message"] == "User registered successfully"
        
        app.dependency_overrides.clear()
    
    def test__register__invalid_email__returns_422(self, client, mock_auth_service):
        # Arrange
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        payload = {"username": "testuser", "email": "invalid-email", "password": "password123"}
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 422
        
        app.dependency_overrides.clear()
    
    def test__register__short_password__returns_422(self, client, mock_auth_service):
        # Arrange
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        payload = {"username": "testuser", "email": "test@example.com", "password": "12345"}
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 422
        
        app.dependency_overrides.clear()


class TestLogin:
    """Test login endpoint"""
    
    def test__login__valid_credentials__returns_tokens(self, client, mock_auth_service):
        # Arrange
        tokens = TokenResponse(access_token="access123", refresh_token="refresh456")
        mock_auth_service.login_user.execute.return_value = tokens
        
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        # Act
        response = client.post("/api/v1/auth/token", data={"username": "testuser", "password": "password123"})
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"
        assert "access_token" in response.json()["data"]
        
        app.dependency_overrides.clear()
    
    def test__login__missing_credentials__returns_422(self, client, mock_auth_service):
        # Arrange
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        # Act
        response = client.post("/api/v1/auth/token", data={})
        
        # Assert
        assert response.status_code == 422
        
        app.dependency_overrides.clear()


class TestRefreshToken:
    """Test refresh token endpoint"""
    
    def test__refresh_token__valid_token__returns_new_tokens(self, client, mock_auth_service):
        # Arrange
        tokens = TokenResponse(access_token="new_access123", refresh_token="new_refresh456")
        mock_auth_service.refresh_token.execute.return_value = tokens
        
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        payload = {"refresh_token": "old_refresh_token"}
        
        # Act
        response = client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Token refreshed successfully"
        assert "access_token" in response.json()["data"]
        
        app.dependency_overrides.clear()


class TestVerifyToken:
    """Test verify token endpoint"""
    
    def test__verify_token__valid_token__returns_user_info(self, client, mock_auth_service):
        # Arrange
        verify_response = VerifyTokenResponse(user_id=1, username="testuser", role="user")
        mock_auth_service.verify_token.execute.return_value = verify_response
        
        app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
        
        payload = {"token": "valid_token"}
        
        # Act
        response = client.post("/api/v1/auth/verify", json=payload)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["user_id"] == 1
        assert response.json()["username"] == "testuser"
        
        app.dependency_overrides.clear()
