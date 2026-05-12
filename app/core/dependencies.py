from typing import Optional

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.core.logger import get_logger

logger = get_logger(__name__)


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
        logger.warning("Request with no credentials")
        raise UnauthorizedException("Not authenticated")

    payload = decode_token(credentials.credentials)
    
    if payload.get("type") != "access":
        logger.warning("Invalid token type: %s", payload.get("type"))
        raise UnauthorizedException("Invalid token type")
    
    return UserContext(
        user_id=payload["user_id"],
        username=payload["sub"],
        role=payload["role"]
    )


def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    """Require admin role"""
    if user.role != "admin":
        logger.warning("Admin access denied for user: %s", user.username)
        raise ForbiddenException("Admin access required")
    return user
