from sqlalchemy.orm import Session

from app.modules.auth.repository import RefreshTokenRepository, UserRepository
from app.modules.auth.use_cases.login_user import LoginUserUseCase
from app.modules.auth.use_cases.refresh_token import RefreshTokenUseCase
from app.modules.auth.use_cases.register_user import RegisterUserUseCase
from app.modules.auth.use_cases.verify_token import VerifyTokenUseCase


class AuthService:
    """Auth service orchestrates use cases"""
    
    def __init__(self, db: Session):
        # Initialize repositories
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)
        
        # Initialize use cases
        self.register_user = RegisterUserUseCase(self.user_repo)
        self.login_user = LoginUserUseCase(self.user_repo, self.token_repo)
        self.refresh_token = RefreshTokenUseCase(self.user_repo, self.token_repo)
        self.verify_token = VerifyTokenUseCase(self.user_repo)
