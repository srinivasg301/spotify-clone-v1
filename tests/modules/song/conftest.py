import pytest
from unittest.mock import MagicMock
from app.modules.song.repository import SongRepository
from app.modules.artist.repository import ArtistRepository
from app.modules.song.use_cases.create_song import CreateSongUseCase
from app.modules.song.use_cases.delete_song import DeleteSongUseCase
from app.modules.song.use_cases.list_songs import ListSongsUseCase


@pytest.fixture
def mock_song_repo():
    """Mock SongRepository for song tests"""
    return MagicMock(spec=SongRepository)


@pytest.fixture
def mock_artist_repo():
    """Mock ArtistRepository for song tests (needed for CreateSong)"""
    return MagicMock(spec=ArtistRepository)


@pytest.fixture
def mock_create_song_use_case():
    """Mock CreateSongUseCase for route tests"""
    return MagicMock(spec=CreateSongUseCase)


@pytest.fixture
def mock_delete_song_use_case():
    """Mock DeleteSongUseCase for route tests"""
    return MagicMock(spec=DeleteSongUseCase)


@pytest.fixture
def mock_list_songs_use_case():
    """Mock ListSongsUseCase for route tests"""
    return MagicMock(spec=ListSongsUseCase)
