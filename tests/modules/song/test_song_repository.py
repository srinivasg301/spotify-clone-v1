from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.modules.song.models import Song
from app.modules.song.repository import SongRepository
from tests.factories.song_factory import SongFactory


class TestSongRepository:
    """Test SongRepository data access methods"""
    
    def test__search_by_title__matching_songs__returns_filtered_songs(self):
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
        mock_offset.all.return_value = [SongFactory.build()]
        
        repo = SongRepository(mock_db)
        
        # Act
        result = repo.search_by_title("test", limit=10, offset=0)
        
        # Assert
        assert len(result) == 1
        mock_db.query.assert_called_once_with(Song)
    
    def test__create_song__valid_data__creates_and_returns_song(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        song_data = SongFactory.build()
        mock_song = MagicMock(spec=Song)
        
        repo = SongRepository(mock_db)
        
        # Act
        result = repo.create_song(
            title=song_data["title"],
            artist_id=song_data["artist_id"],
            duration=song_data["duration"],
            album=song_data["album"],
            thumbnail_url=song_data["thumbnail_url"],
            created_by=song_data["created_by"]
        )
        
        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test__update_song__valid_data__updates_and_returns_song(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_song = MagicMock(spec=Song)
        mock_song.title = "Old Title"
        
        repo = SongRepository(mock_db)
        
        # Act
        result = repo.update_song(mock_song, title="New Title", updated_by="admin")
        
        # Assert
        assert mock_song.title == "New Title"
        mock_db.add.assert_called_once_with(mock_song)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_song)
    
    def test__update_song__partial_data__updates_only_provided_fields(self):
        # Arrange
        mock_db = MagicMock(spec=Session)
        mock_song = MagicMock(spec=Song)
        mock_song.title = "Original Title"
        mock_song.duration = 180
        
        repo = SongRepository(mock_db)
        
        # Act
        result = repo.update_song(mock_song, duration=200)
        
        # Assert
        assert mock_song.title == "Original Title"
        assert mock_song.duration == 200
