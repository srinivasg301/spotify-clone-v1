from typing import Optional

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token


bearer_scheme = HTTPBearer(auto_error=False)


class UserContext(BaseModel):
    """Current user context from JWT token"""
    user_id: int
    username: str
    role: str


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
) -> UserContext:
    """Extract user from JWT token"""
    if not credentials:
        raise UnauthorizedException("Not authenticated")

    # Decode JWT token (no HTTP call needed - same service!)
    payload = decode_token(credentials.credentials)
    
    # Validate token type
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")
    
    return UserContext(
        user_id=payload["user_id"],
        username=payload["sub"],
        role=payload["role"]
    )


def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    """Require admin role"""
    if user.role != "admin":
        raise ForbiddenException("Admin access required")
    return user
