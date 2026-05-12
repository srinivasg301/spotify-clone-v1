import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.use_cases.search_songs import SearchSongsUseCase


@pytest.mark.unit
class TestSearchSongsUseCase:
    """Unit tests for SearchSongsUseCase"""
    
    def test_search_songs_success(self):
        """Test successful song search"""
        # Arrange
        mock_repo = Mock()
        mock_songs = [Song(id=1, title="Test Song", artist_id=1, duration=180)]
        mock_repo.search_by_title.return_value = mock_songs
        
        use_case = SearchSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(title="Test", limit=20, offset=0)
        
        # Assert
        assert len(songs) == 1
        assert songs[0].title == "Test Song"
        mock_repo.search_by_title.assert_called_once_with("Test", limit=20, offset=0)
    
    def test_search_songs_case_insensitive(self):
        """Test search is case-insensitive"""
        # Arrange
        mock_repo = Mock()
        mock_songs = [Song(id=1, title="Test Song", artist_id=1, duration=180)]
        mock_repo.search_by_title.return_value = mock_songs
        
        use_case = SearchSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(title="test", limit=20, offset=0)
        
        # Assert
        assert len(songs) == 1
        assert songs[0].title == "Test Song"
    
    def test_search_songs_partial_match(self):
        """Test partial title matching"""
        # Arrange
        mock_repo = Mock()
        mock_songs = [
            Song(id=1, title="Hey Jude", artist_id=1, duration=180),
            Song(id=2, title="Hey There", artist_id=1, duration=200)
        ]
        mock_repo.search_by_title.return_value = mock_songs
        
        use_case = SearchSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(title="hey", limit=20, offset=0)
        
        # Assert
        assert len(songs) == 2
        assert all("hey" in song.title.lower() for song in songs)
    
    def test_search_songs_no_results(self):
        """Test search with no matching results"""
        # Arrange
        mock_repo = Mock()
        mock_repo.search_by_title.return_value = []
        
        use_case = SearchSongsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No songs found matching"):
            use_case.execute(title="NonExistent", limit=20, offset=0)
    
    def test_search_songs_pagination(self):
        """Test search with pagination"""
        # Arrange
        mock_repo = Mock()
        page1_songs = [Song(id=1, title="Rock Song 0", artist_id=1, duration=180), Song(id=2, title="Rock Song 1", artist_id=1, duration=180)]
        page2_songs = [Song(id=3, title="Rock Song 2", artist_id=1, duration=180), Song(id=4, title="Rock Song 3", artist_id=1, duration=180)]
        mock_repo.search_by_title.side_effect = [page1_songs, page2_songs]
        
        use_case = SearchSongsUseCase(mock_repo)
        
        # Act
        page1 = use_case.execute(title="Rock", limit=2, offset=0)
        page2 = use_case.execute(title="Rock", limit=2, offset=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
