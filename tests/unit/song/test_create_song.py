import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.song.models import Song
from app.modules.song.schemas import CreateSongRequest
from app.modules.song.use_cases.create_song import CreateSongUseCase


@pytest.mark.unit
class TestCreateSongUseCase:
    """Unit tests for CreateSongUseCase"""
    
    def test_create_song_success(self):
        """Test successful song creation"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_song = Song(id=1, title="New Song", artist_id=1, album="New Album", duration=200, created_by="admin")
        
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_song_repo.create_song.return_value = mock_song
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(title="New Song", artist_id=1, album="New Album", duration=200)
        
        # Act
        song = use_case.execute(request, created_by="admin")
        
        # Assert
        assert song.title == "New Song"
        assert song.artist_id == 1
        assert song.album == "New Album"
        assert song.duration == 200
        assert song.created_by == "admin"
        mock_artist_repo.get_by_id.assert_called_once_with(1)
        mock_song_repo.create_song.assert_called_once()
    
    def test_create_song_artist_not_found(self):
        """Test song creation fails when artist doesn't exist"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(title="Orphan Song", artist_id=99999, duration=200)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99999 not found"):
            use_case.execute(request, created_by="admin")
    
    def test_create_song_with_thumbnail(self):
        """Test song creation with thumbnail URL"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_song = Song(id=1, title="Song with Thumbnail", artist_id=1, duration=180, thumbnail_url="https://example.com/thumb.jpg", created_by="admin")
        
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_song_repo.create_song.return_value = mock_song
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(title="Song with Thumbnail", artist_id=1, duration=180, thumbnail_url="https://example.com/thumb.jpg")
        
        # Act
        song = use_case.execute(request, created_by="admin")
        
        # Assert
        assert song.thumbnail_url == "https://example.com/thumb.jpg"
        mock_song_repo.create_song.assert_called_once()
    
    def test_create_song_without_album(self):
        """Test song creation without album"""
        # Arrange
        mock_song_repo = Mock()
        mock_artist_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_song = Song(id=1, title="Single Track", artist_id=1, duration=150, album=None, created_by=None)
        
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_song_repo.create_song.return_value = mock_song
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(title="Single Track", artist_id=1, duration=150)
        
        # Act
        song = use_case.execute(request)
        
        # Assert
        assert song.album is None
        assert song.created_by is None
        mock_song_repo.create_song.assert_called_once()
