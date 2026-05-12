import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.use_cases.list_artists import ListArtistsUseCase


@pytest.mark.unit
class TestListArtistsUseCase:
    """Unit tests for ListArtistsUseCase"""
    
    def test_list_artists_success(self):
        """Test successful artist listing"""
        # Arrange
        mock_repo = Mock()
        mock_artists = [Artist(id=1, name="Test Artist", created_by="admin")]
        mock_repo.get_all.return_value = mock_artists
        
        use_case = ListArtistsUseCase(mock_repo)
        
        # Act
        artists = use_case.execute(limit=20, offset=0)
        
        # Assert
        assert len(artists) == 1
        assert artists[0].name == "Test Artist"
        mock_repo.get_all.assert_called_once_with(limit=20, offset=0)
    
    def test_list_artists_empty(self):
        """Test listing when no artists exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_all.return_value = []
        
        use_case = ListArtistsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No artists found"):
            use_case.execute(limit=20, offset=0)
    
    def test_list_artists_pagination(self):
        """Test artist pagination"""
        # Arrange
        mock_repo = Mock()
        page1_artists = [Artist(id=1, name="Artist 0"), Artist(id=2, name="Artist 1")]
        page2_artists = [Artist(id=3, name="Artist 2"), Artist(id=4, name="Artist 3")]
        mock_repo.get_all.side_effect = [page1_artists, page2_artists]
        
        use_case = ListArtistsUseCase(mock_repo)
        
        # Act
        page1 = use_case.execute(limit=2, offset=0)
        page2 = use_case.execute(limit=2, offset=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].name != page2[0].name
    
    def test_list_artists_limit(self):
        """Test artist limit"""
        # Arrange
        mock_repo = Mock()
        mock_artists = [Artist(id=i, name=f"Artist {i}") for i in range(5)]
        mock_repo.get_all.return_value = mock_artists
        
        use_case = ListArtistsUseCase(mock_repo)
        
        # Act
        artists = use_case.execute(limit=5, offset=0)
        
        # Assert
        assert len(artists) == 5
        mock_repo.get_all.assert_called_once_with(limit=5, offset=0)
