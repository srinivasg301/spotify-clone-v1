import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.use_cases.get_artist_songs import GetArtistSongsUseCase
from app.modules.song.models import Song


@pytest.mark.unit
class TestGetArtistSongsUseCase:
    """Unit tests for GetArtistSongsUseCase"""
    
    def test_get_artist_songs_success(self):
        """Test successful retrieval of artist songs"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_songs = [
            Song(id=1, title="Song 1", artist_id=1, duration=180),
            Song(id=2, title="Song 2", artist_id=1, duration=200)
        ]
        mock_repo.get_by_id.return_value = mock_artist
        mock_repo.get_artist_songs.return_value = mock_songs
        
        use_case = GetArtistSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(1, limit=20, offset=0)
        
        # Assert
        assert len(songs) == 2
        assert songs[0].title == "Song 1"
        assert songs[1].title == "Song 2"
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.get_artist_songs.assert_called_once_with(1, limit=20, offset=0)
    
    def test_get_artist_songs_artist_not_found(self):
        """Test fails when artist doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = GetArtistSongsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99 not found"):
            use_case.execute(99)
    
    def test_get_artist_songs_no_songs(self):
        """Test fails when artist has no songs"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_repo.get_by_id.return_value = mock_artist
        mock_repo.get_artist_songs.return_value = []
        
        use_case = GetArtistSongsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No songs found for artist 'Test Artist'"):
            use_case.execute(1)
    
    def test_get_artist_songs_pagination(self):
        """Test pagination of artist songs"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_songs = [Song(id=1, title="Song 1", artist_id=1, duration=180)]
        mock_repo.get_by_id.return_value = mock_artist
        mock_repo.get_artist_songs.return_value = mock_songs
        
        use_case = GetArtistSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(1, limit=10, offset=5)
        
        # Assert
        assert len(songs) == 1
        mock_repo.get_artist_songs.assert_called_once_with(1, limit=10, offset=5)
