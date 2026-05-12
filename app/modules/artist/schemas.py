from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


# ============================================
# REQUEST SCHEMAS
# ============================================

class CreateArtistRequest(BaseModel):
    """Create artist request"""
    name: str = Field(..., min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise PydanticCustomError(
                'string_too_short',
                'Name cannot be empty or whitespace',
            )
        return v


class UpdateArtistRequest(BaseModel):
    """Update artist request"""
    name: str | None = Field(None, min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise PydanticCustomError(
                    'string_too_short',
                    'Name cannot be empty or whitespace',
                )
        return v


# ============================================
# RESPONSE SCHEMAS
# ============================================

class ArtistResponse(BaseModel):
    """Artist response"""
    id: int
    name: str

    class Config:
        from_attributes = True
