import pytest
from unittest.mock import MagicMock
from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.schemas import CreateArtistRequest, UpdateArtistRequest
from app.modules.artist.use_cases.create_artist import CreateArtistUseCase
from app.modules.artist.use_cases.delete_artist import DeleteArtistUseCase
from app.modules.artist.use_cases.list_artists import ListArtistsUseCase
from app.modules.artist.use_cases.get_artist import GetArtistUseCase
from app.modules.artist.use_cases.update_artist import UpdateArtistUseCase
from app.modules.artist.repository import ArtistRepository
from tests.factories import ArtistFactory


@pytest.mark.unit
class TestCreateArtistUseCase:
    """Tests for CreateArtistUseCase"""
    
    def test__create_artist__with_valid_data__creates_artist_successfully(self, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build()
        mock_artist = Artist(**artist_data)
        mock_artist_repo.create.return_value = mock_artist
        
        use_case = CreateArtistUseCase(mock_artist_repo)
        request = CreateArtistRequest(name=artist_data["name"])
        
        # Act
        result = use_case.execute(request, created_by="admin_user")
        
        # Assert
        assert result.name == artist_data["name"]
        mock_artist_repo.create.assert_called_once_with(
            name=artist_data["name"],
            created_by="admin_user",
            updated_by="admin_user"
        )
    
    def test__create_artist__without_created_by__creates_artist_with_none(self, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build(created_by=None, updated_by=None)
        mock_artist = Artist(**artist_data)
        mock_artist_repo.create.return_value = mock_artist
        
        use_case = CreateArtistUseCase(mock_artist_repo)
        request = CreateArtistRequest(name=artist_data["name"])
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result.name == artist_data["name"]
        mock_artist_repo.create.assert_called_once_with(
            name=artist_data["name"],
            created_by=None,
            updated_by=None
        )


@pytest.mark.unit
class TestDeleteArtistUseCase:
    """Tests for DeleteArtistUseCase"""
    
    def test__delete_artist__with_existing_artist__deletes_successfully(self, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build()
        mock_artist = Artist(**artist_data)
        mock_artist_repo.get_by_id.return_value = mock_artist
        
        use_case = DeleteArtistUseCase(mock_artist_repo)
        
        # Act
        use_case.execute(artist_data["id"])
        
        # Assert
        mock_artist_repo.get_by_id.assert_called_once_with(artist_data["id"])
        mock_artist_repo.delete.assert_called_once_with(mock_artist)
    
    def test__delete_artist__with_nonexistent_artist__raises_not_found_exception(self, mock_artist_repo):
        # Arrange
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = DeleteArtistUseCase(mock_artist_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99999 not found"):
            use_case.execute(99999)
        
        mock_artist_repo.get_by_id.assert_called_once_with(99999)
        mock_artist_repo.delete.assert_not_called()


@pytest.mark.unit
class TestListArtistsUseCase:
    """Tests for ListArtistsUseCase"""
    
    def test__list_artists__with_existing_artists__returns_list_successfully(self, mock_artist_repo):
        # Arrange
        artist_data_list = [ArtistFactory.build() for _ in range(3)]
        mock_artists = [Artist(**data) for data in artist_data_list]
        mock_artist_repo.get_all.return_value = mock_artists
        
        use_case = ListArtistsUseCase(mock_artist_repo)
        
        # Act
        result = use_case.execute(limit=20, offset=0)
        
        # Assert
        assert len(result) == 3
        assert result[0].name == artist_data_list[0]["name"]
        mock_artist_repo.get_all.assert_called_once_with(limit=20, offset=0)
    
    def test__list_artists__with_no_artists__raises_not_found_exception(self, mock_artist_repo):
        # Arrange
        mock_artist_repo.get_all.return_value = []
        
        use_case = ListArtistsUseCase(mock_artist_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No artists found"):
            use_case.execute(limit=20, offset=0)
        
        mock_artist_repo.get_all.assert_called_once_with(limit=20, offset=0)


@pytest.mark.unit
class TestGetArtistUseCase:
    """Tests for GetArtistUseCase"""
    
    def test__get_artist__with_existing_artist__returns_artist_successfully(self, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build()
        mock_artist = Artist(**artist_data)
        mock_artist_repo.get_by_id.return_value = mock_artist
        
        use_case = GetArtistUseCase(mock_artist_repo)
        
        # Act
        result = use_case.execute(artist_data["id"])
        
        # Assert
        assert result.id == artist_data["id"]
        assert result.name == artist_data["name"]
        mock_artist_repo.get_by_id.assert_called_once_with(artist_data["id"])
    
    def test__get_artist__with_nonexistent_artist__raises_not_found_exception(self, mock_artist_repo):
        # Arrange
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = GetArtistUseCase(mock_artist_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99999 not found"):
            use_case.execute(99999)
        
        mock_artist_repo.get_by_id.assert_called_once_with(99999)


@pytest.mark.unit
class TestUpdateArtistUseCase:
    """Tests for UpdateArtistUseCase"""
    
    def test__update_artist__with_valid_data__updates_artist_successfully(self, mock_artist_repo):
        # Arrange
        artist_data = ArtistFactory.build()
        updated_data = ArtistFactory.build(id=artist_data["id"], name="Updated Name")
        mock_artist = Artist(**artist_data)
        mock_updated_artist = Artist(**updated_data)
        mock_artist_repo.get_by_id.return_value = mock_artist
        mock_artist_repo.update.return_value = mock_updated_artist
        
        use_case = UpdateArtistUseCase(mock_artist_repo)
        request = UpdateArtistRequest(name="Updated Name")
        
        # Act
        result = use_case.execute(artist_data["id"], request, updated_by="admin_user")
        
        # Assert
        assert result.name == "Updated Name"
        mock_artist_repo.get_by_id.assert_called_once_with(artist_data["id"])
        mock_artist_repo.update.assert_called_once()
    
    def test__update_artist__with_nonexistent_artist__raises_not_found_exception(self, mock_artist_repo):
        # Arrange
        mock_artist_repo.get_by_id.return_value = None
        
        use_case = UpdateArtistUseCase(mock_artist_repo)
        request = UpdateArtistRequest(name="Updated Name")
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Artist with id 99999 not found"):
            use_case.execute(99999, request, updated_by="admin_user")
        
        mock_artist_repo.get_by_id.assert_called_once_with(99999)
        mock_artist_repo.update.assert_not_called()
