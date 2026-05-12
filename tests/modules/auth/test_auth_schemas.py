import pytest
from pydantic import ValidationError

from app.modules.auth.schemas import RegisterRequest, LoginRequest, UserResponse, TokenResponse


class TestRegisterRequest:
    """Test RegisterRequest validation"""
    
    def test__register_request__valid_data__passes_validation(self):
        # Arrange
        data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
        
        # Act
        request = RegisterRequest(**data)
        
        # Assert
        assert request.username == "testuser"
        assert request.email == "test@example.com"
        assert request.role == "user"
    
    def test__register_request__missing_username__raises_validation_error(self):
        # Arrange
        data = {"email": "test@example.com", "password": "password123"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "username" in str(exc_info.value)
    
    def test__register_request__short_username__raises_validation_error(self):
        # Arrange
        data = {"username": "ab", "email": "test@example.com", "password": "password123"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "username" in str(exc_info.value)
    
    def test__register_request__empty_username__raises_validation_error(self):
        # Arrange
        data = {"username": "   ", "email": "test@example.com", "password": "password123"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "Username cannot be empty or whitespace" in str(exc_info.value)
    
    def test__register_request__invalid_email__raises_validation_error(self):
        # Arrange
        data = {"username": "testuser", "email": "invalid-email", "password": "password123"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "email" in str(exc_info.value)
    
    def test__register_request__email_normalization__converts_to_lowercase(self):
        # Arrange
        data = {"username": "testuser", "email": "TEST@EXAMPLE.COM", "password": "password123"}
        
        # Act
        request = RegisterRequest(**data)
        
        # Assert
        assert request.email == "test@example.com"
    
    def test__register_request__short_password__raises_validation_error(self):
        # Arrange
        data = {"username": "testuser", "email": "test@example.com", "password": "12345"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "password" in str(exc_info.value)
    
    def test__register_request__invalid_role__raises_validation_error(self):
        # Arrange
        data = {"username": "testuser", "email": "test@example.com", "password": "password123", "role": "superuser"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(**data)
        assert "Role must be either 'user' or 'admin'" in str(exc_info.value)
    
    def test__register_request__admin_role__passes_validation(self):
        # Arrange
        data = {"username": "testuser", "email": "test@example.com", "password": "password123", "role": "admin"}
        
        # Act
        request = RegisterRequest(**data)
        
        # Assert
        assert request.role == "admin"


class TestLoginRequest:
    """Test LoginRequest validation"""
    
    def test__login_request__valid_data__passes_validation(self):
        # Arrange
        data = {"username": "testuser", "password": "password123"}
        
        # Act
        request = LoginRequest(**data)
        
        # Assert
        assert request.username == "testuser"
        assert request.password == "password123"


class TestUserResponse:
    """Test UserResponse schema"""
    
    def test__user_response__valid_data__creates_response(self):
        # Arrange
        data = {"id": 1, "username": "testuser", "email": "test@example.com", "role": "user"}
        
        # Act
        response = UserResponse(**data)
        
        # Assert
        assert response.id == 1
        assert response.username == "testuser"
        assert response.email == "test@example.com"
        assert response.role == "user"
    
    def test__user_response__no_password_field__excludes_password(self):
        # Arrange
        data = {"id": 1, "username": "testuser", "email": "test@example.com", "role": "user"}
        
        # Act
        response = UserResponse(**data)
        
        # Assert
        assert not hasattr(response, "password")
        assert not hasattr(response, "hashed_password")


class TestTokenResponse:
    """Test TokenResponse schema"""
    
    def test__token_response__valid_data__creates_response(self):
        # Arrange
        data = {"access_token": "access123", "refresh_token": "refresh456"}
        
        # Act
        response = TokenResponse(**data)
        
        # Assert
        assert response.access_token == "access123"
        assert response.refresh_token == "refresh456"
        assert response.token_type == "bearer"
