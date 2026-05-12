from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from tests.factories.artist_factory import ArtistFactory


class TestArtistRepository:
    """Test ArtistRepository data access methods"""
    
    def test__search_by_name__matching_artists__returns_filtered_artists(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_limit = MagicMock()
        mock_offset = MagicMock()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.limit.return_value = mock_limit
        mock_limit.offset.return_value = mock_offset
        mock_offset.all.return_value = [ArtistFactory.build()]
        
        repo = ArtistRepository(mock_db)
        
        # Act
        result = repo.search_by_name("Beatles", limit=10, offset=0)
        
        # Assert
        assert len(result) == 1
        mock_db.query.assert_called_once_with(Artist)
    
    def test__get_artist_songs__existing_artist__returns_songs(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_limit = MagicMock()
        mock_offset = MagicMock()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.limit.return_value = mock_limit
        mock_limit.offset.return_value = mock_offset
        mock_offset.all.return_value = []
        
        repo = ArtistRepository(mock_db)
        
        # Act
        result = repo.get_artist_songs(artist_id=1, limit=20, offset=0)
        
        # Assert
        assert result == []
        mock_db.query.assert_called_once()
