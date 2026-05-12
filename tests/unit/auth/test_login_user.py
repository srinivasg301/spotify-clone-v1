import pytest
from unittest.mock import Mock, patch

from app.core.exceptions import UnauthorizedException
from app.modules.auth.models import User
from app.modules.auth.use_cases.login_user import LoginUserUseCase


@pytest.mark.unit
class TestLoginUserUseCase:
    """Unit tests for LoginUserUseCase"""
    
    @patch('app.modules.auth.use_cases.login_user.verify_password')
    def test_login_success(self, mock_verify):
        """Test successful login"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_user_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = True
        
        use_case = LoginUserUseCase(mock_user_repo, mock_token_repo)
        
        # Act
        result = use_case.execute("testuser", "testpass123")
        
        # Assert
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"
        mock_user_repo.get_by_username.assert_called_once_with("testuser")
        mock_verify.assert_called_once_with("testpass123", "hashed")
        mock_token_repo.create_token.assert_called_once()
    
    def test_login_invalid_username(self):
        """Test login fails with invalid username"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user_repo.get_by_username.return_value = None
        
        use_case = LoginUserUseCase(mock_user_repo, mock_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid credentials"):
            use_case.execute("nonexistent", "password123")
    
    @patch('app.modules.auth.use_cases.login_user.verify_password')
    def test_login_invalid_password(self, mock_verify):
        """Test login fails with invalid password"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_user_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = False
        
        use_case = LoginUserUseCase(mock_user_repo, mock_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid credentials"):
            use_case.execute("testuser", "wrongpassword")
    
    @patch('app.modules.auth.use_cases.login_user.verify_password')
    def test_login_creates_refresh_token(self, mock_verify):
        """Test login creates refresh token in database"""
        # Arrange
        mock_user_repo = Mock()
        mock_token_repo = Mock()
        mock_user = User(id=1, username="testuser", email="test@example.com", role="user", hashed_password="hashed")
        mock_user_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = True
        
        use_case = LoginUserUseCase(mock_user_repo, mock_token_repo)
        
        # Act
        result = use_case.execute("testuser", "testpass123")
        
        # Assert
        assert result.refresh_token is not None
        mock_token_repo.create_token.assert_called_once()
