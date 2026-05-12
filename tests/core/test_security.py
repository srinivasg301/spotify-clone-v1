import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from freezegun import freeze_time
from jose import jwt
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import UnauthorizedException
from app.core.config import settings


@pytest.mark.unit
class TestPasswordHashing:
    """Tests for password hashing functions"""
    
    def test__hash_password__produces_different_hash_each_call(self):
        # Arrange
        password = "my_secret_password"
        
        # Act
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Assert
        assert hash1 != hash2
    
    def test__verify_password__with_correct_password__returns_true(self):
        # Arrange
        password = "correct_password"
        hashed = hash_password(password)
        
        # Act
        result = verify_password(password, hashed)
        
        # Assert
        assert result is True
    
    def test__verify_password__with_wrong_password__returns_false(self):
        # Arrange
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(correct_password)
        
        # Act
        result = verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False


@pytest.mark.unit
class TestAccessToken:
    """Tests for access token creation and validation"""
    
    @freeze_time("2024-01-01 12:00:00")
    def test__create_access_token__with_valid_data__returns_valid_jwt(self):
        # Arrange
        user_id = 1
        username = "testuser"
        role = "user"
        
        # Act
        token = create_access_token(user_id, username, role)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0
    
    @freeze_time("2024-01-01 12:00:00")
    def test__decode_token__with_valid_access_token__returns_correct_payload(self):
        # Arrange
        user_id = 1
        username = "testuser"
        role = "admin"
        token = create_access_token(user_id, username, role)
        
        # Act
        payload = decode_token(token)
        
        # Assert
        assert payload["sub"] == username
        assert payload["user_id"] == user_id
        assert payload["role"] == role
        assert payload["type"] == "access"
    
    def test__decode_token__with_expired_token__raises_unauthorized_exception(self):
        # Arrange
        with freeze_time("2024-01-01 12:00:00"):
            token = create_access_token(1, "testuser", "user")
        
        # Act & Assert
        with freeze_time("2024-01-02 12:00:00"):
            with pytest.raises(UnauthorizedException, match="Invalid token"):
                decode_token(token)
    
    def test__decode_token__with_tampered_signature__raises_unauthorized_exception(self):
        # Arrange
        token = create_access_token(1, "testuser", "user")
        tampered_token = token[:-10] + "tampered12"
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token"):
            decode_token(tampered_token)
    
    @patch('app.core.security.settings')
    def test__decode_token__with_wrong_secret__raises_unauthorized_exception(self, mock_settings):
        # Arrange
        token = create_access_token(1, "testuser", "user")
        mock_settings.secret_key = "different_secret_key"
        mock_settings.algorithm = settings.algorithm
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token"):
            decode_token(token)
    
    def test__decode_token__with_invalid_token_format__raises_unauthorized_exception(self):
        # Arrange
        invalid_token = "not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token"):
            decode_token(invalid_token)


@pytest.mark.unit
class TestRefreshToken:
    """Tests for refresh token creation and validation"""
    
    @freeze_time("2024-01-01 12:00:00")
    def test__create_refresh_token__returns_token_jti_and_expiry(self):
        # Arrange
        user_id = 1
        username = "testuser"
        
        # Act
        token, jti, expires_at = create_refresh_token(user_id, username)
        
        # Assert
        assert isinstance(token, str)
        assert isinstance(jti, str)
        assert isinstance(expires_at, datetime)
        assert len(jti) > 0
    
    @freeze_time("2024-01-01 12:00:00")
    def test__create_refresh_token__generates_unique_jti_each_call(self):
        # Arrange
        user_id = 1
        username = "testuser"
        
        # Act
        token1, jti1, _ = create_refresh_token(user_id, username)
        token2, jti2, _ = create_refresh_token(user_id, username)
        
        # Assert
        assert jti1 != jti2
        assert token1 != token2
    
    @freeze_time("2024-01-01 12:00:00")
    def test__decode_token__with_valid_refresh_token__returns_correct_payload(self):
        # Arrange
        user_id = 1
        username = "testuser"
        token, jti, _ = create_refresh_token(user_id, username)
        
        # Act
        payload = decode_token(token)
        
        # Assert
        assert payload["sub"] == username
        assert payload["user_id"] == user_id
        assert payload["type"] == "refresh"
        assert payload["jti"] == jti
