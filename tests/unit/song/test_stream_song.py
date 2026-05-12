import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.use_cases.stream_song import StreamSongUseCase


@pytest.mark.unit
class TestStreamSongUseCase:
    """Unit tests for StreamSongUseCase"""
    
    def test_stream_song_success(self):
        """Test successful stream URL generation"""
        # Arrange
        mock_repo = Mock()
        mock_song = Song(id=1, title="Test Song", artist_id=1, duration=180)
        mock_repo.get_by_id.return_value = mock_song
        
        use_case = StreamSongUseCase(mock_repo)
        
        # Act
        result = use_case.execute(1)
        
        # Assert
        assert result.id == 1
        assert result.title == "Test Song"
        assert result.stream_url == "https://cdn.spotify-clone.com/stream/1"
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_stream_song_not_found(self):
        """Test stream fails when song doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = StreamSongUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99 not found"):
            use_case.execute(99)
    
    def test_stream_song_url_format(self):
        """Test stream URL format is correct"""
        # Arrange
        mock_repo = Mock()
        mock_song = Song(id=42, title="Another Song", artist_id=1, duration=200)
        mock_repo.get_by_id.return_value = mock_song
        
        use_case = StreamSongUseCase(mock_repo)
        
        # Act
        result = use_case.execute(42)
        
        # Assert
        assert "cdn.spotify-clone.com" in result.stream_url
        assert "/stream/42" in result.stream_url
