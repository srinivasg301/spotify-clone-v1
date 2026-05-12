from datetime import datetime

from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.modules.auth.repository import RefreshTokenRepository, UserRepository
from app.modules.auth.schemas import TokenResponse


class RefreshTokenUseCase:
    """Use case: Refresh access token"""
    
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo
    
    def execute(self, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token JWT
        
        Returns:
            New access and refresh tokens
        
        Raises:
            UnauthorizedException: If token is invalid, revoked, or expired
        """
        # Decode refresh token
        payload = decode_token(refresh_token)
        
        # Validate token type
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid token type")
        
        jti = payload.get("jti")
        user_id = payload.get("user_id")
        
        # Get token from database
        db_token = self.token_repo.get_by_jti(jti)
        
        # Check if token exists and not revoked
        if not db_token or db_token.revoked:
            raise UnauthorizedException("Token revoked")
        
        # Check if token expired
        if db_token.expires_at < datetime.utcnow():
            raise UnauthorizedException("Token expired")
        
        # Revoke old token (token rotation for security)
        self.token_repo.revoke_token(db_token)
        
        # Get user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")
        
        # Create new tokens
        access_token = create_access_token(user.id, user.username, user.role)
        new_refresh_token, new_jti, new_expires_at = create_refresh_token(user.id, user.username)
        
        # Store new refresh token
        self.token_repo.create_token(user.id, new_jti, new_expires_at)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )
