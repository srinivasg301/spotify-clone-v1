import pytest
from unittest.mock import Mock, patch

from app.core.exceptions import UnauthorizedException
from app.modules.auth.models import User
from app.modules.auth.use_cases.verify_token import VerifyTokenUseCase


@pytest.mark.unit
class TestVerifyTokenUseCase:
    """Unit tests for VerifyTokenUseCase"""
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test_verify_token_success(self, mock_decode):
        """Test successful token verification"""
        # Arrange
        mock_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_decode.return_value = {"user_id": 1, "username": "testuser", "role": "user", "type": "access"}
        mock_repo.get_by_id.return_value = mock_user
        
        use_case = VerifyTokenUseCase(mock_repo)
        
        # Act
        result = use_case.execute("valid.access.token")
        
        # Assert
        assert result.user_id == 1
        assert result.username == "testuser"
        assert result.role == "user"
        mock_decode.assert_called_once_with("valid.access.token")
        mock_repo.get_by_id.assert_called_once_with(1)
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test_verify_token_invalid_type(self, mock_decode):
        """Test verification fails with refresh token"""
        # Arrange
        mock_repo = Mock()
        mock_decode.return_value = {"user_id": 1, "username": "testuser", "type": "refresh"}
        
        use_case = VerifyTokenUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token type"):
            use_case.execute("refresh.token.here")
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test_verify_token_invalid_token(self, mock_decode):
        """Test verification fails with invalid token"""
        # Arrange
        mock_repo = Mock()
        mock_decode.side_effect = UnauthorizedException("Invalid token")
        
        use_case = VerifyTokenUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid token"):
            use_case.execute("invalid.token.here")
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test_verify_token_user_not_found(self, mock_decode):
        """Test verification fails when user doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_decode.return_value = {"user_id": 99999, "username": "nonexistent", "role": "user", "type": "access"}
        mock_repo.get_by_id.return_value = None
        
        use_case = VerifyTokenUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="User not found"):
            use_case.execute("valid.token.nonexistent.user")
