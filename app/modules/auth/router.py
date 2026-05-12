from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.schemas import (
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    VerifyTokenRequest,
    VerifyTokenResponse,
)
from app.modules.auth.service import AuthService
from app.shared.base_schema import SuccessResponse

router = APIRouter(tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get auth service"""
    return AuthService(db)


@router.post("/register", response_model=SuccessResponse[UserResponse], status_code=201)
def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[UserResponse]:
    """Register new user"""
    user = service.register_user.execute(request)
    return SuccessResponse(
        data=UserResponse.model_validate(user),
        message="User registered successfully"
    )


@router.post("/token", response_model=SuccessResponse[TokenResponse])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[TokenResponse]:
    """Login and get tokens (OAuth2 compatible)"""
    tokens = service.login_user.execute(form_data.username, form_data.password)
    return SuccessResponse(data=tokens, message="Login successful")


@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
def refresh_token(
    request: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[TokenResponse]:
    """Refresh access token"""
    tokens = service.refresh_token.execute(request.refresh_token)
    return SuccessResponse(data=tokens, message="Token refreshed successfully")


@router.post("/verify", response_model=VerifyTokenResponse)
def verify_token(
    request: VerifyTokenRequest,
    service: AuthService = Depends(get_auth_service),
) -> VerifyTokenResponse:
    """Verify access token (internal use)"""
    return service.verify_token.execute(request.token)
