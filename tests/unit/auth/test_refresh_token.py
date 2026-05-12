import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from app.core.exceptions import UnauthorizedException
from app.modules.auth.models import RefreshToken, User
from app.modules.auth.use_cases.refresh_token import RefreshTokenUseCase


@pytest.mark.unit
class TestRefreshTokenUseCase:
    """Unit tests for RefreshTokenUseCase"""
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test_refresh_token_success(self, mock_decode):
        """Test successful token refresh"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_db_token = RefreshToken(id=1, user_id=1, jti="jti123", expires_at=datetime.utcnow() + timedelta(days=7), revoked=False)
        
        mock_decode.return_value = {"sub": 1, "username": "testuser", "type": "refresh", "jti": "jti123"}
        mock_user_repo.get_by_id.return_value = mock_user
        mock_token_repo.get_by_jti.return_value = mock_db_token
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_token_repo)
        
        # Act
        result = use_case.execute("valid.refresh.token")
        
        # Assert
        assert result.access_token is not None
        assert result.refresh_token is not None
        mock_token_repo.revoke_token.assert_called_once_with(mock_db_token)
        mock_token_repo.create_token.assert_called_once()
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test_refresh_token_revokes_old_token(self, mock_decode):
        """Test refresh revokes old token (token rotation)"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_db_token = RefreshToken(id=1, user_id=1, jti="jti123", expires_at=datetime.utcnow() + timedelta(days=7), revoked=False)
        
        mock_decode.return_value = {"sub": 1, "username": "testuser", "type": "refresh", "jti": "jti123"}
        mock_user_repo.get_by_id.return_value = mock_user
        mock_token_repo.get_by_jti.return_value = mock_db_token
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_token_repo)
        
        # Act
        use_case.execute("valid.refresh.token")
        
        # Assert
        mock_token_repo.revoke_token.assert_called_once_with(mock_db_token)
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test_refresh_token_invalid_type(self, mock_decode):
        """Test refresh fails with access token"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_decode.return_value = {"sub": 1, "username": "testuser", "type": "access"}
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token type"):
            use_case.execute("access.token.here")
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test_refresh_token_revoked(self, mock_decode):
        """Test refresh fails with revoked token"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_db_token = RefreshToken(id=1, user_id=1, jti="jti123", expires_at=datetime.utcnow() + timedelta(days=7), revoked=True)
        
        mock_decode.return_value = {"sub": 1, "username": "testuser", "type": "refresh", "jti": "jti123"}
        mock_token_repo.get_by_jti.return_value = mock_db_token
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Token revoked"):
            use_case.execute("revoked.token.here")
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test_refresh_token_expired(self, mock_decode):
        """Test refresh fails with expired token"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_db_token = RefreshToken(id=1, user_id=1, jti="jti123", expires_at=datetime.utcnow() - timedelta(days=1), revoked=False)
        
        mock_decode.return_value = {"sub": 1, "username": "testuser", "type": "refresh", "jti": "jti123"}
        mock_token_repo.get_by_jti.return_value = mock_db_token
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Token expired"):
            use_case.execute("expired.token.here")
