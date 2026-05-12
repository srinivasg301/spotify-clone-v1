from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.artist.repository import ArtistRepository
from app.modules.artist.service import ArtistService


class TestArtistService:
    """Test ArtistService initialization and orchestration"""
    
    def test__artist_service__initialization__creates_repository_and_use_cases(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        
        # Act
        service = ArtistService(mock_db)
        
        # Assert
        assert isinstance(service.artist_repo, ArtistRepository)
        assert service.create_artist is not None
        assert service.update_artist is not None
        assert service.delete_artist is not None
        assert service.list_artists is not None
        assert service.get_artist is not None
        assert service.search_artists is not None
        assert service.get_artist_songs is not None
