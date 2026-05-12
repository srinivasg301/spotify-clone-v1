import pytest
from unittest.mock import Mock

from app.modules.artist.models import Artist
from app.modules.artist.schemas import CreateArtistRequest
from app.modules.artist.use_cases.create_artist import CreateArtistUseCase


@pytest.mark.unit
class TestCreateArtistUseCase:
    """Unit tests for CreateArtistUseCase"""
    
    def test_create_artist_success(self):
        """Test successful artist creation"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=1, name="New Artist", created_by="admin", updated_by="admin")
        mock_repo.create.return_value = mock_artist
        
        use_case = CreateArtistUseCase(mock_repo)
        request = CreateArtistRequest(name="New Artist")
        
        # Act
        artist = use_case.execute(request, created_by="admin")
        
        # Assert
        assert artist.name == "New Artist"
        assert artist.created_by == "admin"
        assert artist.updated_by == "admin"
        assert artist.id == 1
        mock_repo.create.assert_called_once()
    
    def test_create_artist_without_creator(self):
        """Test artist creation without creator info"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=2, name="Anonymous Artist", created_by=None, updated_by=None)
        mock_repo.create.return_value = mock_artist
        
        use_case = CreateArtistUseCase(mock_repo)
        request = CreateArtistRequest(name="Anonymous Artist")
        
        # Act
        artist = use_case.execute(request)
        
        # Assert
        assert artist.name == "Anonymous Artist"
        assert artist.created_by is None
        assert artist.updated_by is None
    
    def test_create_artist_strips_whitespace(self):
        """Test artist name is trimmed"""
        # Arrange
        mock_repo = Mock()
        mock_artist = Artist(id=3, name="Spaced Artist", created_by="admin", updated_by="admin")
        mock_repo.create.return_value = mock_artist
        
        use_case = CreateArtistUseCase(mock_repo)
        request = CreateArtistRequest(name="  Spaced Artist  ")
        
        # Act
        artist = use_case.execute(request, created_by="admin")
        
        # Assert
        assert artist.name == "Spaced Artist"
