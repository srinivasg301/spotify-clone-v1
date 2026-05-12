from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.artist.repository import ArtistRepository
from app.modules.song.repository import SongRepository
from app.modules.song.service import SongService


class TestSongService:
    """Test SongService initialization and orchestration"""
    
    def test__song_service__initialization__creates_repositories_and_use_cases(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        
        # Act
        service = SongService(mock_db)
        
        # Assert
        assert isinstance(service.song_repo, SongRepository)
        assert isinstance(service.artist_repo, ArtistRepository)
        assert service.create_song is not None
        assert service.update_song is not None
        assert service.delete_song is not None
        assert service.list_songs is not None
        assert service.get_song is not None
        assert service.search_songs is not None
        assert service.stream_song is not None
