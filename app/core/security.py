import hashlib
import uuid
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UnauthorizedException


# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using SHA256 + bcrypt"""
    password = hashlib.sha256(password.encode()).hexdigest()
    return bcrypt_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hashed version"""
    plain = hashlib.sha256(plain.encode()).hexdigest()
    return bcrypt_context.verify(plain, hashed)


def create_access_token(user_id: int, username: str, role: str) -> str:
    """Create JWT access token"""
    payload = {
        "sub": username,
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: int, username: str) -> tuple[str, str, datetime]:
    """Create JWT refresh token with unique ID"""
    jti = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": username,
        "user_id": user_id,
        "type": "refresh",
        "jti": jti,
        "exp": expires,
    }

    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, jti, expires


def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise UnauthorizedException("Invalid token")
