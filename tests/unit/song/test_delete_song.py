import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.use_cases.delete_song import DeleteSongUseCase


@pytest.mark.unit
class TestDeleteSongUseCase:
    """Unit tests for DeleteSongUseCase"""
    
    def test_delete_song_success(self):
        """Test successful song deletion"""
        # Arrange
        mock_repo = Mock()
        mock_song = Song(id=1, title="Test Song", artist_id=1, duration=180)
        mock_repo.get_by_id.return_value = mock_song
        
        use_case = DeleteSongUseCase(mock_repo)
        
        # Act
        use_case.execute(1)
        
        # Assert
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.delete.assert_called_once_with(mock_song)
    
    def test_delete_song_not_found(self):
        """Test delete fails when song doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = DeleteSongUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99 not found"):
            use_case.execute(99)
        mock_repo.delete.assert_not_called()
