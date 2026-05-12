import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.modules.auth.models import User, RefreshToken
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.use_cases.register_user import RegisterUserUseCase
from app.modules.auth.use_cases.login_user import LoginUserUseCase
from app.modules.auth.use_cases.refresh_token import RefreshTokenUseCase
from app.modules.auth.use_cases.verify_token import VerifyTokenUseCase
from app.modules.auth.repository import UserRepository, RefreshTokenRepository
from tests.factories import UserFactory, RefreshTokenFactory, RevokedRefreshTokenFactory, ExpiredRefreshTokenFactory


@pytest.mark.unit
class TestRegisterUserUseCase:
    """Tests for RegisterUserUseCase"""
    
    @patch('app.modules.auth.use_cases.register_user.hash_password')
    def test__register_user__with_valid_data__creates_user_successfully(self, mock_hash, mock_user_repo):
        # Arrange
        mock_user_repo.get_by_username.return_value = None
        mock_user_repo.get_by_email.return_value = None
        user_data = UserFactory.build()
        mock_user = User(**user_data)
        mock_user_repo.create_user.return_value = mock_user
        mock_hash.return_value = "hashed_password_123"
        
        use_case = RegisterUserUseCase(mock_user_repo)
        request = RegisterRequest(
            username=user_data["username"],
            email=user_data["email"],
            password="plaintext_password",
            role="user"
        )
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result.username == user_data["username"]
        assert result.email == user_data["email"]
        mock_user_repo.get_by_username.assert_called_once_with(user_data["username"])
        mock_user_repo.get_by_email.assert_called_once_with(user_data["email"])
        mock_hash.assert_called_once_with("plaintext_password")
        mock_user_repo.create_user.assert_called_once()
    
    def test__register_user__with_duplicate_username__raises_bad_request_exception(self, mock_user_repo):
        # Arrange
        existing_user_data = UserFactory.build()
        existing_user = User(**existing_user_data)
        mock_user_repo.get_by_username.return_value = existing_user
        
        use_case = RegisterUserUseCase(mock_user_repo)
        request = RegisterRequest(
            username=existing_user_data["username"],
            email="different@example.com",
            password="password123",
            role="user"
        )
        
        # Act & Assert
        with pytest.raises(BadRequestException, match="Username already exists"):
            use_case.execute(request)
        
        mock_user_repo.get_by_username.assert_called_once_with(existing_user_data["username"])
        mock_user_repo.get_by_email.assert_not_called()
        mock_user_repo.create_user.assert_not_called()
    
    def test__register_user__with_duplicate_email__raises_bad_request_exception(self, mock_user_repo):
        # Arrange
        existing_user_data = UserFactory.build()
        existing_user = User(**existing_user_data)
        mock_user_repo.get_by_username.return_value = None
        mock_user_repo.get_by_email.return_value = existing_user
        
        use_case = RegisterUserUseCase(mock_user_repo)
        request = RegisterRequest(
            username="different_user",
            email=existing_user_data["email"],
            password="password123",
            role="user"
        )
        
        # Act & Assert
        with pytest.raises(BadRequestException, match="Email already exists"):
            use_case.execute(request)
        
        mock_user_repo.get_by_username.assert_called_once_with("different_user")
        mock_user_repo.get_by_email.assert_called_once_with(existing_user_data["email"])
        mock_user_repo.create_user.assert_not_called()


@pytest.mark.unit
class TestLoginUserUseCase:
    """Tests for LoginUserUseCase"""
    
    @patch('app.modules.auth.use_cases.login_user.verify_password')
    @patch('app.modules.auth.use_cases.login_user.create_access_token')
    @patch('app.modules.auth.use_cases.login_user.create_refresh_token')
    def test__login_user__with_valid_credentials__returns_tokens_successfully(
        self, mock_create_refresh, mock_create_access, mock_verify, mock_user_repo, mock_refresh_token_repo
    ):
        # Arrange
        user_data = UserFactory.build()
        mock_user = User(**user_data)
        mock_user_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = True
        mock_create_access.return_value = "access_token_123"
        mock_create_refresh.return_value = ("refresh_token_456", "jti_789", datetime.utcnow() + timedelta(days=7))
        
        use_case = LoginUserUseCase(mock_user_repo, mock_refresh_token_repo)
        
        # Act
        result = use_case.execute(user_data["username"], "correct_password")
        
        # Assert
        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_456"
        assert result.token_type == "bearer"
        mock_user_repo.get_by_username.assert_called_once_with(user_data["username"])
        mock_verify.assert_called_once_with("correct_password", user_data["hashed_password"])
        mock_refresh_token_repo.create_token.assert_called_once()
    
    def test__login_user__with_nonexistent_username__raises_unauthorized_exception(
        self, mock_user_repo, mock_refresh_token_repo
    ):
        # Arrange
        mock_user_repo.get_by_username.return_value = None
        
        use_case = LoginUserUseCase(mock_user_repo, mock_refresh_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid credentials"):
            use_case.execute("nonexistent_user", "any_password")
        
        mock_user_repo.get_by_username.assert_called_once_with("nonexistent_user")
        mock_refresh_token_repo.create_token.assert_not_called()
    
    @patch('app.modules.auth.use_cases.login_user.verify_password')
    def test__login_user__with_incorrect_password__raises_unauthorized_exception(
        self, mock_verify, mock_user_repo, mock_refresh_token_repo
    ):
        # Arrange
        user_data = UserFactory.build()
        mock_user = User(**user_data)
        mock_user_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = False
        
        use_case = LoginUserUseCase(mock_user_repo, mock_refresh_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Invalid credentials"):
            use_case.execute(user_data["username"], "wrong_password")
        
        mock_verify.assert_called_once_with("wrong_password", user_data["hashed_password"])
        mock_refresh_token_repo.create_token.assert_not_called()


@pytest.mark.unit
class TestRefreshTokenUseCase:
    """Tests for RefreshTokenUseCase"""
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    @patch('app.modules.auth.use_cases.refresh_token.create_access_token')
    @patch('app.modules.auth.use_cases.refresh_token.create_refresh_token')
    def test__refresh_token__with_valid_token__returns_new_tokens_successfully(
        self, mock_create_refresh, mock_create_access, mock_decode, mock_user_repo, mock_refresh_token_repo
    ):
        # Arrange
        user_data = UserFactory.build()
        token_data = RefreshTokenFactory.build(user_id=user_data["id"])
        mock_user = User(**user_data)
        mock_token = RefreshToken(**token_data)
        
        mock_decode.return_value = {
            "sub": user_data["username"],
            "user_id": user_data["id"],
            "type": "refresh",
            "jti": token_data["jti"]
        }
        mock_user_repo.get_by_id.return_value = mock_user
        mock_refresh_token_repo.get_by_jti.return_value = mock_token
        mock_create_access.return_value = "new_access_token"
        expires_at = datetime.utcnow() + timedelta(days=7)
        mock_create_refresh.return_value = ("new_refresh_token", "new_jti", expires_at)
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_refresh_token_repo)
        
        # Act
        result = use_case.execute("old_refresh_token")
        
        # Assert
        assert result.access_token == "new_access_token"
        assert result.refresh_token == "new_refresh_token"
        mock_refresh_token_repo.revoke_token.assert_called_once_with(mock_token)
        mock_refresh_token_repo.create_token.assert_called_once()
    
    @patch('app.modules.auth.use_cases.refresh_token.decode_token')
    def test__refresh_token__with_revoked_token__raises_unauthorized_exception(
        self, mock_decode, mock_user_repo, mock_refresh_token_repo
    ):
        # Arrange
        token_data = RevokedRefreshTokenFactory.build()
        mock_token = RefreshToken(**token_data)
        
        mock_decode.return_value = {
            "sub": "testuser",
            "user_id": 1,
            "type": "refresh",
            "jti": token_data["jti"]
        }
        mock_refresh_token_repo.get_by_jti.return_value = mock_token
        
        use_case = RefreshTokenUseCase(mock_user_repo, mock_refresh_token_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="Token revoked"):
            use_case.execute("revoked_refresh_token")
        
        mock_refresh_token_repo.create_token.assert_not_called()


@pytest.mark.unit
class TestVerifyTokenUseCase:
    """Tests for VerifyTokenUseCase"""
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test__verify_token__with_valid_access_token__returns_user_info_successfully(
        self, mock_decode, mock_user_repo
    ):
        # Arrange
        user_data = UserFactory.build()
        mock_user = User(**user_data)
        
        mock_decode.return_value = {
            "user_id": user_data["id"],
            "sub": user_data["username"],
            "role": user_data["role"],
            "type": "access"
        }
        mock_user_repo.get_by_id.return_value = mock_user
        
        use_case = VerifyTokenUseCase(mock_user_repo)
        
        # Act
        result = use_case.execute("valid_access_token")
        
        # Assert
        assert result.user_id == user_data["id"]
        assert result.username == user_data["username"]
        assert result.role == user_data["role"]
        mock_decode.assert_called_once_with("valid_access_token")
        mock_user_repo.get_by_id.assert_called_once_with(user_data["id"])
    
    @patch('app.modules.auth.use_cases.verify_token.decode_token')
    def test__verify_token__with_nonexistent_user__raises_unauthorized_exception(
        self, mock_decode, mock_user_repo
    ):
        # Arrange
        mock_decode.return_value = {
            "user_id": 99999,
            "sub": "nonexistent_user",
            "role": "user",
            "type": "access"
        }
        mock_user_repo.get_by_id.return_value = None
        
        use_case = VerifyTokenUseCase(mock_user_repo)
        
        # Act & Assert
        with pytest.raises(UnauthorizedException, match="User not found"):
            use_case.execute("valid_token_but_user_deleted")
        
        mock_user_repo.get_by_id.assert_called_once_with(99999)
