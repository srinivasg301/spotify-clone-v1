from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError


# ============================================
# REQUEST SCHEMAS
# ============================================

class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field("user")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise PydanticCustomError(
                'string_too_short',
                'Username cannot be empty or whitespace',
            )
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ["user", "admin"]:
            raise PydanticCustomError(
                'value_error',
                "Role must be either 'user' or 'admin'",
            )
        return v

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class LoginRequest(BaseModel):
    """User login request (OAuth2 compatible)"""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class VerifyTokenRequest(BaseModel):
    """Token verification request"""
    token: str


# ============================================
# RESPONSE SCHEMAS
# ============================================

class UserResponse(BaseModel):
    """User response"""
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerifyTokenResponse(BaseModel):
    """Token verification response"""
    user_id: int
    username: str
    role: str
