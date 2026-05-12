from typing import List, TypeVar

from app.shared.base_schema import PaginatedResponse, PaginationMeta


T = TypeVar("T")


def paginate(
    data: List[T],
    total: int,
    limit: int,
    offset: int,
    message: str = None
) -> PaginatedResponse[T]:
    """
    Create paginated response
    
    Args:
        data: List of items for current page
        total: Total count of items
        limit: Items per page
        offset: Starting position
        message: Optional message
    
    Returns:
        PaginatedResponse with data and metadata
    """
    has_more = (offset + limit) < total
    
    meta = PaginationMeta(
        total=total,
        limit=limit,
        offset=offset,
        has_more=has_more
    )
    
    return PaginatedResponse(
        data=data,
        meta=meta,
        message=message
    )


def validate_pagination(limit: int, offset: int) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters
    
    Args:
        limit: Requested items per page
        offset: Requested starting position
    
    Returns:
        Validated (limit, offset) tuple
    """
    # Ensure limit is between 1 and 100
    limit = max(1, min(limit, 100))
    
    # Ensure offset is non-negative
    offset = max(0, offset)
    
    return limit, offset
