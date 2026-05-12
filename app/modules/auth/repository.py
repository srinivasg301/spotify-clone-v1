from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.modules.auth.models import RefreshToken, User
from app.shared.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """User data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, username: str, email: str, hashed_password: str, role: str = "user") -> User:
        """Create new user"""
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Refresh token data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(RefreshToken, db)
    
    def create_token(self, user_id: int, jti: str, expires_at: datetime) -> RefreshToken:
        """Create new refresh token"""
        token = RefreshToken(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
            revoked=False
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def get_by_jti(self, jti: str) -> Optional[RefreshToken]:
        """Get refresh token by JTI"""
        return self.db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    
    def revoke_token(self, token: RefreshToken) -> None:
        """Revoke refresh token"""
        token.revoked = True
        self.db.add(token)
        self.db.commit()
