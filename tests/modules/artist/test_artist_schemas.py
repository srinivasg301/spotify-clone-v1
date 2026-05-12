import pytest
from pydantic import ValidationError

from app.modules.artist.schemas import CreateArtistRequest, UpdateArtistRequest, ArtistResponse


class TestCreateArtistRequest:
    """Test CreateArtistRequest validation"""
    
    def test__create_artist_request__valid_data__passes_validation(self):
        # Arrange
        data = {"name": "The Beatles"}
        
        # Act
        request = CreateArtistRequest(**data)
        
        # Assert
        assert request.name == "The Beatles"
    
    def test__create_artist_request__missing_name__raises_validation_error(self):
        # Arrange
        data = {}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateArtistRequest(**data)
        assert "name" in str(exc_info.value)
    
    def test__create_artist_request__empty_name__raises_validation_error(self):
        # Arrange
        data = {"name": "   "}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateArtistRequest(**data)
        assert "Name cannot be empty or whitespace" in str(exc_info.value)
    
    def test__create_artist_request__name_with_whitespace__strips_whitespace(self):
        # Arrange
        data = {"name": "  The Beatles  "}
        
        # Act
        request = CreateArtistRequest(**data)
        
        # Assert
        assert request.name == "The Beatles"


class TestUpdateArtistRequest:
    """Test UpdateArtistRequest validation"""
    
    def test__update_artist_request__valid_data__passes_validation(self):
        # Arrange
        data = {"name": "Updated Artist"}
        
        # Act
        request = UpdateArtistRequest(**data)
        
        # Assert
        assert request.name == "Updated Artist"
    
    def test__update_artist_request__empty_name__raises_validation_error(self):
        # Arrange
        data = {"name": "   "}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UpdateArtistRequest(**data)
        assert "Name cannot be empty or whitespace" in str(exc_info.value)
    
    def test__update_artist_request__no_data__passes_validation(self):
        # Arrange
        data = {}
        
        # Act
        request = UpdateArtistRequest(**data)
        
        # Assert
        assert request.name is None


class TestArtistResponse:
    """Test ArtistResponse schema"""
    
    def test__artist_response__valid_data__creates_response(self):
        # Arrange
        data = {"id": 1, "name": "The Beatles"}
        
        # Act
        response = ArtistResponse(**data)
        
        # Assert
        assert response.id == 1
        assert response.name == "The Beatles"
