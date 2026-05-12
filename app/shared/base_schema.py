from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper"""
    success: bool = True
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper"""
    success: bool = False
    data: None = None
    message: str
    errors: Optional[list] = []


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    total: int
    limit: int
    offset: int
    has_more: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    success: bool = True
    data: list[T]
    meta: PaginationMeta
    message: Optional[str] = None
