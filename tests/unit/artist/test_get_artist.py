import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.use_cases.get_artist import GetArtistUseCase


@pytest.mark.unit
class TestGetArtistUseCase:
    """Unit tests for GetArtistUseCase"""
    
    def test_get_artist_success(self):
        """Test successful artist retrieval"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist", created_by="admin")
        mock_repo.get_by_id.return_value = mock_artist
        
        use_case = GetArtistUseCase(mock_repo)
        
        # Act
        artist = use_case.execute(1)
        
        # Assert
        assert artist.id == 1
        assert artist.name == "Test Artist"
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_get_artist_not_found(self):
        """Test get fails when artist doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = GetArtistUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99 not found"):
            use_case.execute(99)
