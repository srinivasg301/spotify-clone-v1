import pytest
from unittest.mock import MagicMock
from app.modules.artist.repository import ArtistRepository
from app.modules.artist.use_cases.create_artist import CreateArtistUseCase
from app.modules.artist.use_cases.delete_artist import DeleteArtistUseCase
from app.modules.artist.use_cases.list_artists import ListArtistsUseCase


@pytest.fixture
def mock_artist_repo():
    """Mock ArtistRepository for artist tests"""
    return MagicMock(spec=ArtistRepository)


@pytest.fixture
def mock_create_artist_use_case():
    """Mock CreateArtistUseCase for route tests"""
    return MagicMock(spec=CreateArtistUseCase)


@pytest.fixture
def mock_delete_artist_use_case():
    """Mock DeleteArtistUseCase for route tests"""
    return MagicMock(spec=DeleteArtistUseCase)


@pytest.fixture
def mock_list_artists_use_case():
    """Mock ListArtistsUseCase for route tests"""
    return MagicMock(spec=ListArtistsUseCase)
