import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.schemas import UpdateArtistRequest
from app.modules.artist.use_cases.update_artist import UpdateArtistUseCase


@pytest.mark.unit
class TestUpdateArtistUseCase:
    """Unit tests for UpdateArtistUseCase"""
    
    def test_update_artist_success(self):
        """Test successful artist update"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Old Name", created_by="admin")
        mock_updated = Artist(id=1, name="New Name", updated_by="admin")
        mock_repo.get_by_id.return_value = mock_artist
        mock_repo.update.return_value = mock_updated
        
        use_case = UpdateArtistUseCase(mock_repo)
        request = UpdateArtistRequest(name="New Name")
        
        # Act
        artist = use_case.execute(1, request, updated_by="admin")
        
        # Assert
        assert artist.name == "New Name"
        assert artist.updated_by == "admin"
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once_with(mock_artist, name="New Name", updated_by="admin")
    
    def test_update_artist_not_found(self):
        """Test update fails when artist doesn't exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        use_case = UpdateArtistUseCase(mock_repo)
        request = UpdateArtistRequest(name="New Name")
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99 not found"):
            use_case.execute(99, request, updated_by="admin")
    
    def test_update_artist_without_updater(self):
        """Test artist update without updater info"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="Old Name")
        mock_updated = Artist(id=1, name="New Name", updated_by=None)
        mock_repo.get_by_id.return_value = mock_artist
        mock_repo.update.return_value = mock_updated
        
        use_case = UpdateArtistUseCase(mock_repo)
        request = UpdateArtistRequest(name="New Name")
        
        # Act
        artist = use_case.execute(1, request)
        
        # Assert
        assert artist.name == "New Name"
        assert artist.updated_by is None
