import pytest
from unittest.mock import Mock, patch

from app.core.exceptions import BadRequestException
from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.use_cases.register_user import RegisterUserUseCase


@pytest.mark.unit
class TestRegisterUserUseCase:
    """Unit tests for RegisterUserUseCase"""
    
    @patch('app.modules.auth.use_cases.register_user.hash_password')
    def test_register_user_success(self, mock_hash):
        """Test successful user registration"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = None
        mock_user = User(id=1, username="newuser", email="newuser@example.com", role="user", hashed_password="hashed")
        mock_repo.create_user.return_value = mock_user
        mock_hash.return_value = "hashed"
        
        use_case = RegisterUserUseCase(mock_repo)
        request = RegisterRequest(username="newuser", email="newuser@example.com", password="password123", role="user")
        
        # Act
        user = use_case.execute(request)
        
        # Assert
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.role == "user"
        mock_repo.get_by_username.assert_called_once_with("newuser")
        mock_repo.get_by_email.assert_called_once_with("newuser@example.com")
        mock_repo.create_user.assert_called_once()
        mock_hash.assert_called_once_with("password123")
    
    def test_register_user_duplicate_username(self):
        """Test registration fails with duplicate username"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = User(id=1, username="existing", email="other@example.com", role="user", hashed_password="hashed")
        
        use_case = RegisterUserUseCase(mock_repo)
        request = RegisterRequest(username="existing", email="new@example.com", password="password123", role="user")
        
        # Act & Assert
        with pytest.raises(BadRequestException, match="Username already exists"):
            use_case.execute(request)
        mock_repo.get_by_username.assert_called_once_with("existing")
    
    def test_register_user_duplicate_email(self):
        """Test registration fails with duplicate email"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = User(id=1, username="other", email="existing@example.com", role="user", hashed_password="hashed")
        
        use_case = RegisterUserUseCase(mock_repo)
        request = RegisterRequest(username="newuser", email="existing@example.com", password="password123", role="user")
        
        # Act & Assert
        with pytest.raises(BadRequestException, match="Email already exists"):
            use_case.execute(request)
        mock_repo.get_by_email.assert_called_once_with("existing@example.com")
    
    @patch('app.modules.auth.use_cases.register_user.hash_password')
    def test_register_admin_user(self, mock_hash):
        """Test admin user registration"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = None
        mock_user = User(id=1, username="adminuser", email="admin@example.com", role="admin", hashed_password="hashed")
        mock_repo.create_user.return_value = mock_user
        mock_hash.return_value = "hashed"
        
        use_case = RegisterUserUseCase(mock_repo)
        request = RegisterRequest(username="adminuser", email="admin@example.com", password="password123", role="admin")
        
        # Act
        user = use_case.execute(request)
        
        # Assert
        assert user.role == "admin"
