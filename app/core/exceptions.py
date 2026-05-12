from fastapi import HTTPException, status

from app.core.logger import get_logger

logger = get_logger(__name__)


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        logger.warning("NotFoundException: %s", detail)
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Access forbidden"):
        logger.warning("ForbiddenException: %s", detail)
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        logger.warning("UnauthorizedException: %s", detail)
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ValidationException(HTTPException):
    def __init__(self, detail: str = "Validation error"):
        logger.warning("ValidationException: %s", detail)
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        logger.warning("BadRequestException: %s", detail)
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
