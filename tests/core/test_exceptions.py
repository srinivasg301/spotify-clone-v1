import pytest
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
)


@pytest.mark.unit
class TestCustomExceptions:
    """Tests for custom HTTP exceptions"""
    
    def test__not_found_exception__has_correct_status_code(self):
        # Arrange & Act
        exception = NotFoundException("Resource not found")
        
        # Assert
        assert exception.status_code == 404
        assert exception.detail == "Resource not found"
    
    def test__bad_request_exception__has_correct_status_code(self):
        # Arrange & Act
        exception = BadRequestException("Invalid request")
        
        # Assert
        assert exception.status_code == 400
        assert exception.detail == "Invalid request"
    
    def test__unauthorized_exception__has_correct_status_code(self):
        # Arrange & Act
        exception = UnauthorizedException("Unauthorized access")
        
        # Assert
        assert exception.status_code == 401
        assert exception.detail == "Unauthorized access"
    
    def test__forbidden_exception__has_correct_status_code(self):
        # Arrange & Act
        exception = ForbiddenException("Access forbidden")
        
        # Assert
        assert exception.status_code == 403
        assert exception.detail == "Access forbidden"
    
    def test__validation_exception__has_correct_status_code(self):
        # Arrange & Act
        exception = ValidationException("Validation failed")
        
        # Assert
        assert exception.status_code == 422
        assert exception.detail == "Validation failed"
