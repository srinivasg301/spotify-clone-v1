import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.song.models import Song
from app.modules.song.schemas import UpdateSongRequest
from app.modules.song.use_cases.update_song import UpdateSongUseCase


@pytest.mark.unit
class TestUpdateSongUseCase:
    """Unit tests for UpdateSongUseCase"""
    
    def test_update_song_success(self):
        """Test successful song update"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_song = Song(id=1, title="Old Title", artist_id=1, duration=180)
        mock_updated = Song(id=1, title="New Title", artist_id=1, duration=200, updated_by="admin")
        mock_song_repo.get_by_id.return_value = mock_song
        mock_song_repo.update_song.return_value = mock_updated
        
        use_case = UpdateSongUseCase(mock_song_repo, mock_artist_repo)
        request = UpdateSongRequest(title="New Title", duration=200)
        
        # Act
        song = use_case.execute(1, request, updated_by="admin")
        
        # Assert
        assert song.title == "New Title"
        assert song.duration == 200
        assert song.updated_by == "admin"
        mock_song_repo.get_by_id.assert_called_once_with(1)
        mock_song_repo.update_song.assert_called_once()
    
    def test_update_song_not_found(self):
        """Test update fails when song doesn't exist"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_song_repo.get_by_id.return_value = None
        
        use_case = UpdateSongUseCase(mock_song_repo, mock_artist_repo)
        request = UpdateSongRequest(title="New Title")
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99 not found"):
            use_case.execute(99, request)
    
    def test_update_song_with_new_artist(self):
        """Test song update with artist change"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_song = Song(id=1, title="Test Song", artist_id=1, duration=180)
        mock_artist = Artist(id=2, name="New Artist")
        mock_updated = Song(id=1, title="Test Song", artist_id=2, duration=180)
        mock_song_repo.get_by_id.return_value = mock_song
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_song_repo.update_song.return_value = mock_updated
        
        use_case = UpdateSongUseCase(mock_song_repo, mock_artist_repo)
        request = UpdateSongRequest(artist_id=2)
        
        # Act
        song = use_case.execute(1, request, updated_by="admin")
        
        # Assert
        assert song.artist_id == 2
        mock_artist_repo.get_by_id.assert_called_once_with(2)
    
    def test_update_song_artist_not_found(self):
        """Test update fails when new artist doesn't exist"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_song = Song(id=1, title="Test Song", artist_id=1, duration=180)
        mock_song_repo.get_by_id.return_value = mock_song
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = UpdateSongUseCase(mock_song_repo, mock_artist_repo)
        request = UpdateSongRequest(artist_id=99)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99 not found"):
            use_case.execute(1, request)
