from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.modules.auth.repository import RefreshTokenRepository, UserRepository
from app.modules.auth.schemas import TokenResponse


class LoginUserUseCase:
    """Use case: User login"""
    
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo
    
    def execute(self, username: str, password: str) -> TokenResponse:
        """
        Authenticate user and generate tokens
        
        Args:
            username: Username
            password: Plain password
        
        Returns:
            Access and refresh tokens
        
        Raises:
            UnauthorizedException: If credentials are invalid
        """
        # Get user by username
        user = self.user_repo.get_by_username(username)
        
        # Verify credentials
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid credentials")
        
        # Create access token
        access_token = create_access_token(user.id, user.username, user.role)
        
        # Create refresh token
        refresh_token, jti, expires_at = create_refresh_token(user.id, user.username)
        
        # Store refresh token in database
        self.token_repo.create_token(user.id, jti, expires_at)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
