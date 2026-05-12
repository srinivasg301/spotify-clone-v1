from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic_core import PydanticCustomError


# ============================================
# REQUEST SCHEMAS
# ============================================

class CreateSongRequest(BaseModel):
    """Create song request"""
    title: str = Field(..., min_length=1, max_length=255)
    artist_id: int = Field(..., gt=0)
    album: Optional[str] = Field(None, max_length=255)
    duration: int = Field(..., gt=0)
    thumbnail_url: Optional[HttpUrl] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise PydanticCustomError(
                'string_too_short',
                'Title cannot be empty or whitespace',
            )
        return v

    @field_validator("album")
    @classmethod
    def validate_album(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


class UpdateSongRequest(BaseModel):
    """Update song request"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    artist_id: Optional[int] = Field(None, gt=0)
    album: Optional[str] = Field(None, max_length=255)
    duration: Optional[int] = Field(None, gt=0)
    thumbnail_url: Optional[HttpUrl] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise PydanticCustomError(
                    'string_too_short',
                    'Title cannot be empty or whitespace',
                )
        return v

    @field_validator("album")
    @classmethod
    def validate_album(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


# ============================================
# RESPONSE SCHEMAS
# ============================================

class SongResponse(BaseModel):
    """Song response"""
    id: int
    title: str
    artist_id: int
    album: Optional[str]
    duration: int
    thumbnail_url: Optional[str]

    class Config:
        from_attributes = True


class SongStreamResponse(BaseModel):
    """Song stream response"""
    id: int
    title: str
    stream_url: str

    class Config:
        from_attributes = True
