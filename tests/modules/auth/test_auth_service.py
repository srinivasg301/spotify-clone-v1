from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.auth.repository import RefreshTokenRepository, UserRepository
from app.modules.auth.service import AuthService


class TestAuthService:
    """Test AuthService initialization and orchestration"""
    
    def test__auth_service__initialization__creates_repositories_and_use_cases(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        
        # Act
        service = AuthService(mock_db)
        
        # Assert
        assert isinstance(service.user_repo, UserRepository)
        assert isinstance(service.token_repo, RefreshTokenRepository)
        assert service.register_user is not None
        assert service.login_user is not None
        assert service.refresh_token is not None
        assert service.verify_token is not None
