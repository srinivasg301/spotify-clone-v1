import pytest
from pydantic import ValidationError

from app.modules.song.schemas import CreateSongRequest, UpdateSongRequest, SongResponse


class TestCreateSongRequest:
    """Test CreateSongRequest validation"""
    
    def test__create_song_request__valid_data__passes_validation(self):
        # Arrange
        data = {"title": "Test Song", "artist_id": 1, "duration": 180}
        
        # Act
        request = CreateSongRequest(**data)
        
        # Assert
        assert request.title == "Test Song"
        assert request.artist_id == 1
        assert request.duration == 180
    
    def test__create_song_request__missing_title__raises_validation_error(self):
        # Arrange
        data = {"artist_id": 1, "duration": 180}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateSongRequest(**data)
        assert "title" in str(exc_info.value)
    
    def test__create_song_request__empty_title__raises_validation_error(self):
        # Arrange
        data = {"title": "   ", "artist_id": 1, "duration": 180}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateSongRequest(**data)
        assert "Title cannot be empty or whitespace" in str(exc_info.value)
    
    def test__create_song_request__zero_artist_id__raises_validation_error(self):
        # Arrange
        data = {"title": "Test Song", "artist_id": 0, "duration": 180}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateSongRequest(**data)
        assert "artist_id" in str(exc_info.value)
    
    def test__create_song_request__zero_duration__raises_validation_error(self):
        # Arrange
        data = {"title": "Test Song", "artist_id": 1, "duration": 0}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateSongRequest(**data)
        assert "duration" in str(exc_info.value)
    
    def test__create_song_request__whitespace_album__converts_to_none(self):
        # Arrange
        data = {"title": "Test Song", "artist_id": 1, "duration": 180, "album": "   "}
        
        # Act
        request = CreateSongRequest(**data)
        
        # Assert
        assert request.album is None


class TestUpdateSongRequest:
    """Test UpdateSongRequest validation"""
    
    def test__update_song_request__valid_partial_data__passes_validation(self):
        # Arrange
        data = {"title": "Updated Song"}
        
        # Act
        request = UpdateSongRequest(**data)
        
        # Assert
        assert request.title == "Updated Song"
        assert request.artist_id is None
    
    def test__update_song_request__empty_title__raises_validation_error(self):
        # Arrange
        data = {"title": "   "}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UpdateSongRequest(**data)
        assert "Title cannot be empty or whitespace" in str(exc_info.value)
    
    def test__update_song_request__zero_duration__raises_validation_error(self):
        # Arrange
        data = {"duration": 0}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UpdateSongRequest(**data)
        assert "duration" in str(exc_info.value)


class TestSongResponse:
    """Test SongResponse schema"""
    
    def test__song_response__valid_data__creates_response(self):
        # Arrange
        data = {"id": 1, "title": "Test Song", "artist_id": 1, "album": "Test Album", "duration": 180, "thumbnail_url": "https://example.com/thumb.jpg"}
        
        # Act
        response = SongResponse(**data)
        
        # Assert
        assert response.id == 1
        assert response.title == "Test Song"
        assert response.artist_id == 1
