from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import UserContext, get_current_user, require_admin
from app.main import app
from app.modules.artist.router import get_artist_service
from tests.factories.artist_factory import ArtistFactory
from tests.factories.song_factory import SongFactory


@pytest.fixture
def mock_artist_service():
    """Mock artist service"""
    return MagicMock()


@pytest.fixture
def mock_user():
    """Mock regular user"""
    return UserContext(user_id=1, username="testuser", role="user")


@pytest.fixture
def mock_admin():
    """Mock admin user"""
    return UserContext(user_id=1, username="admin", role="admin")


@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)


class TestListArtists:
    """Test list artists endpoint"""
    
    def test__list_artists__authenticated_user__returns_artists(self, client, mock_artist_service, mock_user):
        # Arrange
        artists = [ArtistFactory.build(), ArtistFactory.build()]
        mock_artist_service.list_artists.execute.return_value = artists
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/artists")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
        
        app.dependency_overrides.clear()
    
    def test__list_artists__with_pagination__passes_limit_and_offset(self, client, mock_artist_service, mock_user):
        # Arrange
        mock_artist_service.list_artists.execute.return_value = []
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/artists?limit=10&offset=5")
        
        # Assert
        assert response.status_code == 200
        mock_artist_service.list_artists.execute.assert_called_once_with(limit=10, offset=5)
        
        app.dependency_overrides.clear()


class TestSearchArtists:
    """Test search artists endpoint"""
    
    def test__search_artists__valid_query__returns_matching_artists(self, client, mock_artist_service, mock_user):
        # Arrange
        artists = [ArtistFactory.build()]
        mock_artist_service.search_artists.execute.return_value = artists
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/artists/search?name=Beatles")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["data"]) == 1
        
        app.dependency_overrides.clear()


class TestGetArtist:
    """Test get artist endpoint"""
    
    def test__get_artist__valid_id__returns_artist(self, client, mock_artist_service, mock_user):
        # Arrange
        artist = ArtistFactory.build()
        mock_artist_service.get_artist.execute.return_value = artist
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/artists/1")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["data"]["id"] == artist["id"]
        
        app.dependency_overrides.clear()


class TestGetArtistSongs:
    """Test get artist songs endpoint"""
    
    def test__get_artist_songs__valid_id__returns_songs(self, client, mock_artist_service, mock_user):
        # Arrange
        songs = [SongFactory.build(), SongFactory.build()]
        mock_artist_service.get_artist_songs.execute.return_value = songs
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/artists/1/songs")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
        
        app.dependency_overrides.clear()


class TestCreateArtist:
    """Test create artist endpoint"""
    
    def test__create_artist__admin_user__creates_artist(self, client, mock_artist_service, mock_admin):
        # Arrange
        artist = ArtistFactory.build()
        mock_artist_service.create_artist.execute.return_value = artist
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"name": "New Artist"}
        
        # Act
        response = client.post("/api/v1/artists", json=payload)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["message"] == "Artist created successfully"
        
        app.dependency_overrides.clear()
    
    def test__create_artist__invalid_data__returns_422(self, client, mock_artist_service, mock_admin):
        # Arrange
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"name": ""}
        
        # Act
        response = client.post("/api/v1/artists", json=payload)
        
        # Assert
        assert response.status_code == 422
        
        app.dependency_overrides.clear()


class TestUpdateArtist:
    """Test update artist endpoint"""
    
    def test__update_artist__admin_user__updates_artist(self, client, mock_artist_service, mock_admin):
        # Arrange
        artist = ArtistFactory.build()
        mock_artist_service.update_artist.execute.return_value = artist
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"name": "Updated Artist"}
        
        # Act
        response = client.put("/api/v1/artists/1", json=payload)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Artist updated successfully"
        
        app.dependency_overrides.clear()


class TestDeleteArtist:
    """Test delete artist endpoint"""
    
    def test__delete_artist__admin_user__deletes_artist(self, client, mock_artist_service, mock_admin):
        # Arrange
        mock_artist_service.delete_artist.execute.return_value = None
        
        app.dependency_overrides[get_artist_service] = lambda: mock_artist_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        # Act
        response = client.delete("/api/v1/artists/1")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Artist deleted successfully"
        
        app.dependency_overrides.clear()
