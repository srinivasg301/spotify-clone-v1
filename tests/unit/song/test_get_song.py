import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.use_cases.get_song import GetSongUseCase


@pytest.mark.unit
class TestGetSongUseCase:
    """Unit tests for GetSongUseCase"""
    
    def test_get_song_success(self):
        """Test successful song retrieval"""
        # Arrange
        mock_repo = Mock()
        mock_song = Song(id=1, title="Test Song", artist_id=1, duration=180, album="Test Album")
        mock_repo.get_by_id.return_value = mock_song
        
        use_case = GetSongUseCase(mock_repo)
        
        # Act
        song = use_case.execute(1)
        
        # Assert
        assert song.id == 1
        assert song.title == "Test Song"
        assert song.album == "Test Album"
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_get_song_not_found(self):
        """Test get fails when song doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = GetSongUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99 not found"):
            use_case.execute(99)
