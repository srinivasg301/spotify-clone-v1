from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.auth.models import RefreshToken, User
from app.modules.auth.repository import RefreshTokenRepository, UserRepository
from tests.factories.user_factory import UserFactory
from tests.factories.refresh_token_factory import RefreshTokenFactory


class TestUserRepository:
    """Test UserRepository data access methods"""
    
    def test__get_by_username__existing_user__returns_user(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        user_data = UserFactory.build()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = user_data
        
        repo = UserRepository(mock_db)
        
        # Act
        result = repo.get_by_username("testuser")
        
        # Assert
        assert result == user_data
        mock_db.query.assert_called_once_with(User)
    
    def test__get_by_email__existing_user__returns_user(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        user_data = UserFactory.build()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = user_data
        
        repo = UserRepository(mock_db)
        
        # Act
        result = repo.get_by_email("test@example.com")
        
        # Assert
        assert result == user_data
        mock_db.query.assert_called_once_with(User)
    
    def test__create_user__valid_data__creates_and_returns_user(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        
        repo = UserRepository(mock_db)
        
        # Act
        result = repo.create_user(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed123",
            role="user"
        )
        
        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


class TestRefreshTokenRepository:
    """Test RefreshTokenRepository data access methods"""
    
    def test__create_token__valid_data__creates_and_returns_token(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        repo = RefreshTokenRepository(mock_db)
        
        # Act
        result = repo.create_token(user_id=1, jti="unique-jti", expires_at=expires_at)
        
        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test__get_by_jti__existing_token__returns_token(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        token_data = RefreshTokenFactory.build()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = token_data
        
        repo = RefreshTokenRepository(mock_db)
        
        # Act
        result = repo.get_by_jti("unique-jti")
        
        # Assert
        assert result == token_data
        mock_db.query.assert_called_once_with(RefreshToken)
    
    def test__revoke_token__existing_token__revokes_token(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_token = MagicMock(spec=RefreshToken)
        mock_token.revoked = False
        
        repo = RefreshTokenRepository(mock_db)
        
        # Act
        repo.revoke_token(mock_token)
        
        # Assert
        assert mock_token.revoked is True
        mock_db.add.assert_called_once_with(mock_token)
        mock_db.commit.assert_called_once()
