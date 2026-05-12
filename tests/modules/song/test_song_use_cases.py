import pytest
from unittest.mock import MagicMock
from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from app.modules.song.models import Song
from app.modules.song.schemas import CreateSongRequest, UpdateSongRequest
from app.modules.song.use_cases.create_song import CreateSongUseCase
from app.modules.song.use_cases.delete_song import DeleteSongUseCase
from app.modules.song.use_cases.list_songs import ListSongsUseCase
from app.modules.song.use_cases.get_song import GetSongUseCase
from app.modules.song.use_cases.update_song import UpdateSongUseCase
from app.modules.song.use_cases.stream_song import StreamSongUseCase
from app.modules.song.repository import SongRepository
from tests.factories import ArtistFactory, SongFactory


@pytest.mark.unit
class TestCreateSongUseCase:
    """Tests for CreateSongUseCase"""
    
    def test__create_song__with_valid_data__creates_song_successfully(self, mock_song_repo, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build()
        song_data = SongFactory.build(artist_id=artist_data["id"])
        mock_artist = Artist(**artist_data)
        mock_song = Song(**song_data)
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_song_repo.create_song.return_value = mock_song
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(
            title=song_data["title"],
            artist_id=artist_data["id"],
            album=song_data["album"],
            duration=song_data["duration"]
        )
        
        # Act
        result = use_case.execute(request, created_by="admin_user")
        
        # Assert
        assert result.title == song_data["title"]
        assert result.artist_id == artist_data["id"]
        mock_artist_repo.get_by_id.assert_called_once_with(artist_data["id"])
        mock_song_repo.create_song.assert_called_once()
    
    def test__create_song__with_nonexistent_artist__raises_not_found_exception(self, mock_song_repo, mock_artist_repo):
        # Arrange
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = CreateSongUseCase(mock_song_repo, mock_artist_repo)
        request = CreateSongRequest(
            title="Test Song",
            artist_id=99999,
            duration=180
        )
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99999 not found"):
            use_case.execute(request, created_by="admin_user")
        
        mock_artist_repo.get_by_id.assert_called_once_with(99999)
        mock_song_repo.create_song.assert_not_called()


@pytest.mark.unit
class TestDeleteSongUseCase:
    """Tests for DeleteSongUseCase"""
    
    def test__delete_song__with_existing_song__deletes_successfully(self, mock_song_repo):
        # Arrange
        song_data = SongFactory.build()
        mock_song = Song(**song_data)
        mock_song_repo.get_by_id.return_value = mock_song
        
        use_case = DeleteSongUseCase(mock_song_repo)
        
        # Act
        use_case.execute(song_data["id"])
        
        # Assert
        mock_song_repo.get_by_id.assert_called_once_with(song_data["id"])
        mock_song_repo.delete.assert_called_once_with(mock_song)
    
    def test__delete_song__with_nonexistent_song__raises_not_found_exception(self, mock_song_repo):
        # Arrange
        mock_song_repo.get_by_id.return_value = None
        
        use_case = DeleteSongUseCase(mock_song_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99999 not found"):
            use_case.execute(99999)
        
        mock_song_repo.get_by_id.assert_called_once_with(99999)
        mock_song_repo.delete.assert_not_called()


@pytest.mark.unit
class TestListSongsUseCase:
    """Tests for ListSongsUseCase"""
    
    def test__list_songs__with_existing_songs__returns_list_successfully(self, mock_song_repo):
        # Arrange
        song_data_list = [SongFactory.build() for _ in range(3)]
        mock_songs = [Song(**data) for data in song_data_list]
        mock_song_repo.get_all.return_value = mock_songs
        
        use_case = ListSongsUseCase(mock_song_repo)
        
        # Act
        result = use_case.execute(limit=20, offset=0)
        
        # Assert
        assert len(result) == 3
        assert result[0].title == song_data_list[0]["title"]
        mock_song_repo.get_all.assert_called_once_with(limit=20, offset=0)
    
    def test__list_songs__with_no_songs__raises_not_found_exception(self, mock_song_repo):
        # Arrange
        mock_song_repo.get_all.return_value = []
        
        use_case = ListSongsUseCase(mock_song_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No songs found"):
            use_case.execute(limit=20, offset=0)
        
        mock_song_repo.get_all.assert_called_once_with(limit=20, offset=0)


@pytest.mark.unit
class TestGetSongUseCase:
    """Tests for GetSongUseCase"""
    
    def test__get_song__with_existing_song__returns_song_successfully(self, mock_song_repo):
        # Arrange
        song_data = SongFactory.build()
        mock_song = Song(**song_data)
        mock_song_repo.get_by_id.return_value = mock_song
        
        use_case = GetSongUseCase(mock_song_repo)
        
        # Act
        result = use_case.execute(song_data["id"])
        
        # Assert
        assert result.id == song_data["id"]
        assert result.title == song_data["title"]
        mock_song_repo.get_by_id.assert_called_once_with(song_data["id"])
    
    def test__get_song__with_nonexistent_song__raises_not_found_exception(self, mock_song_repo):
        # Arrange
        mock_song_repo.get_by_id.return_value = None
        
        use_case = GetSongUseCase(mock_song_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99999 not found"):
            use_case.execute(99999)
        
        mock_song_repo.get_by_id.assert_called_once_with(99999)


@pytest.mark.unit
class TestStreamSongUseCase:
    """Tests for StreamSongUseCase"""
    
    def test__stream_song__with_existing_song__returns_stream_url_successfully(self, mock_song_repo):
        # Arrange
        song_data = SongFactory.build()
        mock_song = Song(**song_data)
        mock_song_repo.get_by_id.return_value = mock_song
        
        use_case = StreamSongUseCase(mock_song_repo)
        
        # Act
        result = use_case.execute(song_data["id"])
        
        # Assert
        assert result.id == song_data["id"]
        assert result.title == song_data["title"]
        assert "cdn.spotify-clone.com" in result.stream_url
        assert f"/stream/{song_data['id']}" in result.stream_url
        mock_song_repo.get_by_id.assert_called_once_with(song_data["id"])
    
    def test__stream_song__with_nonexistent_song__raises_not_found_exception(self, mock_song_repo):
        # Arrange
        mock_song_repo.get_by_id.return_value = None
        
        use_case = StreamSongUseCase(mock_song_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Song with id 99999 not found"):
            use_case.execute(99999)
        
        mock_song_repo.get_by_id.assert_called_once_with(99999)
