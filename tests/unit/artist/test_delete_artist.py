import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.use_cases.delete_artist import DeleteArtistUseCase


@pytest.mark.unit
class TestDeleteArtistUseCase:
    """Unit tests for DeleteArtistUseCase"""
    
    def test_delete_artist_success(self):
        """Test successful artist deletion"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Test Artist")
        mock_repo.get_by_id.return_value = mock_artist
        
        use_case = DeleteArtistUseCase(mock_repo)
        
        # Act
        use_case.execute(1)
        
        # Assert
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.delete.assert_called_once_with(mock_artist)
    
    def test_delete_artist_not_found(self):
        """Test delete fails when artist doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = DeleteArtistUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99 not found"):
            use_case.execute(99)
        mock_repo.delete.assert_not_called()
