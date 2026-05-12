import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.use_cases.search_artists import SearchArtistsUseCase


@pytest.mark.unit
class TestSearchArtistsUseCase:
    """Unit tests for SearchArtistsUseCase"""
    
    def test_search_artists_success(self):
        """Test successful artist search"""
        # Arrange
        mock_repo = Mock()
        mock_artists = [Artist(id=1, name="Test Artist", created_by="admin")]
        mock_repo.search_by_name.return_value = mock_artists
        
        use_case = SearchArtistsUseCase(mock_repo)
        
        # Act
        artists = use_case.execute(name="Test", limit=20, offset=0)
        
        # Assert
        assert len(artists) == 1
        assert artists[0].name == "Test Artist"
        mock_repo.search_by_name.assert_called_once_with("Test", limit=20, offset=0)
    
    def test_search_artists_case_insensitive(self):
        """Test search is case-insensitive"""
        # Arrange
        mock_repo = Mock()
        mock_artists = [Artist(id=1, name="Test Artist", created_by="admin")]
        mock_repo.search_by_name.return_value = mock_artists
        
        use_case = SearchArtistsUseCase(mock_repo)
        
        # Act
        artists = use_case.execute(name="test", limit=20, offset=0)
        
        # Assert
        assert len(artists) == 1
        assert artists[0].name == "Test Artist"
    
    def test_search_artists_partial_match(self):
        """Test partial name matching"""
        # Arrange
        mock_repo = Mock()
        mock_artists = [
            Artist(id=1, name="The Beatles", created_by="admin"),
            Artist(id=2, name="Beatles Revival", created_by="admin")
        ]
        mock_repo.search_by_name.return_value = mock_artists
        
        use_case = SearchArtistsUseCase(mock_repo)
        
        # Act
        artists = use_case.execute(name="beatles", limit=20, offset=0)
        
        # Assert
        assert len(artists) == 2
        assert all("beatles" in artist.name.lower() for artist in artists)
    
    def test_search_artists_no_results(self):
        """Test search with no matching results"""
        # Arrange
        mock_repo = Mock()
        mock_repo.search_by_name.return_value = []
        
        use_case = SearchArtistsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No artists found matching"):
            use_case.execute(name="NonExistent", limit=20, offset=0)
    
    def test_search_artists_pagination(self):
        """Test search with pagination"""
        # Arrange
        mock_repo = Mock()
        page1_artists = [Artist(id=1, name="Rock Band 0"), Artist(id=2, name="Rock Band 1")]
        page2_artists = [Artist(id=3, name="Rock Band 2"), Artist(id=4, name="Rock Band 3")]
        mock_repo.search_by_name.side_effect = [page1_artists, page2_artists]
        
        use_case = SearchArtistsUseCase(mock_repo)
        
        # Act
        page1 = use_case.execute(name="Rock", limit=2, offset=0)
        page2 = use_case.execute(name="Rock", limit=2, offset=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
