from app.core.exceptions import BadRequestException
from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import RegisterRequest
from app.core.logger import get_logger

logger = get_logger(__name__)


class RegisterUserUseCase:
    """Use case: Register new user"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def execute(self, request: RegisterRequest) -> User:
        """
        Register new user
        
        Args:
            request: Registration data
        
        Returns:
            Created user
        
        Raises:
            BadRequestException: If username or email already exists
        """
        # Check if username exists
        if self.user_repo.get_by_username(request.username):
            raise BadRequestException("Username already exists")
        
        # Check if email exists
        if self.user_repo.get_by_email(request.email):
            raise BadRequestException("Email already exists")
        
        # Hash password
        hashed_password = hash_password(request.password)
        
        # Create user
        user = self.user_repo.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role=request.role
        )
        logger.info("User registered: username=%s, role=%s", user.username, user.role)
        return user
