import pytest
from unittest.mock import MagicMock
from app.modules.auth.repository import UserRepository, RefreshTokenRepository
from app.modules.auth.use_cases.register_user import RegisterUserUseCase
from app.modules.auth.use_cases.login_user import LoginUserUseCase
from app.modules.auth.use_cases.refresh_token import RefreshTokenUseCase
from app.modules.auth.use_cases.verify_token import VerifyTokenUseCase


@pytest.fixture
def mock_user_repo():
    """Mock UserRepository for auth tests"""
    return MagicMock(spec=UserRepository)


@pytest.fixture
def mock_refresh_token_repo():
    """Mock RefreshTokenRepository for auth tests"""
    return MagicMock(spec=RefreshTokenRepository)


@pytest.fixture
def mock_register_use_case():
    """Mock RegisterUserUseCase for route tests"""
    return MagicMock(spec=RegisterUserUseCase)


@pytest.fixture
def mock_login_use_case():
    """Mock LoginUserUseCase for route tests"""
    return MagicMock(spec=LoginUserUseCase)


@pytest.fixture
def mock_refresh_token_use_case():
    """Mock RefreshTokenUseCase for route tests"""
    return MagicMock(spec=RefreshTokenUseCase)


@pytest.fixture
def mock_verify_token_use_case():
    """Mock VerifyTokenUseCase for route tests"""
    return MagicMock(spec=VerifyTokenUseCase)
