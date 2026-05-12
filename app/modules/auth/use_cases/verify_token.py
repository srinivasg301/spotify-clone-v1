from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import VerifyTokenResponse
from app.core.logger import get_logger

logger = get_logger(__name__)


class VerifyTokenUseCase:
    """Use case: Verify access token"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def execute(self, token: str) -> VerifyTokenResponse:
        """
        Verify access token and return user info
        
        Args:
            token: Access token JWT
        
        Returns:
            User information from token
        
        Raises:
            UnauthorizedException: If token is invalid or user not found
        """
        # Decode token
        payload = decode_token(token)
        
        # Validate token type
        if payload.get("type") != "access":
            raise UnauthorizedException("Invalid token type")
        
        # Get user
        user = self.user_repo.get_by_id(payload["user_id"])
        if not user:
            raise UnauthorizedException("User not found")
        
        logger.info("Token verified for user_id=%s", user.id)
        return VerifyTokenResponse(
            user_id=user.id,
            username=user.username,
            role=user.role
        )
