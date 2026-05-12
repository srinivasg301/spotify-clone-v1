from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import UserContext, get_current_user, require_admin
from app.main import app
from app.modules.song.router import get_song_service
from app.modules.song.schemas import SongStreamResponse
from tests.factories.song_factory import SongFactory


@pytest.fixture
def mock_song_service():
    """Mock song service"""
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


class TestListSongs:
    """Test list songs endpoint"""
    
    def test__list_songs__authenticated_user__returns_songs(self, client, mock_song_service, mock_user):
        # Arrange
        songs = [SongFactory.build(), SongFactory.build()]
        mock_song_service.list_songs.execute.return_value = songs
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/songs")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
        
        app.dependency_overrides.clear()
    
    def test__list_songs__with_pagination__passes_limit_and_offset(self, client, mock_song_service, mock_user):
        # Arrange
        mock_song_service.list_songs.execute.return_value = []
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/songs?limit=10&offset=5")
        
        # Assert
        assert response.status_code == 200
        mock_song_service.list_songs.execute.assert_called_once_with(limit=10, offset=5)
        
        app.dependency_overrides.clear()


class TestSearchSongs:
    """Test search songs endpoint"""
    
    def test__search_songs__valid_query__returns_matching_songs(self, client, mock_song_service, mock_user):
        # Arrange
        songs = [SongFactory.build()]
        mock_song_service.search_songs.execute.return_value = songs
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/songs/search?title=test")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["data"]) == 1
        
        app.dependency_overrides.clear()


class TestGetSong:
    """Test get song endpoint"""
    
    def test__get_song__valid_id__returns_song(self, client, mock_song_service, mock_user):
        # Arrange
        song = SongFactory.build()
        mock_song_service.get_song.execute.return_value = song
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/songs/1")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["data"]["id"] == song["id"]
        
        app.dependency_overrides.clear()


class TestStreamSong:
    """Test stream song endpoint"""
    
    def test__stream_song__valid_id__returns_stream_url(self, client, mock_song_service, mock_user):
        # Arrange
        stream = SongStreamResponse(id=1, title="Test Song", stream_url="https://stream.example.com/1")
        mock_song_service.stream_song.execute.return_value = stream
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[get_current_user] = lambda: mock_user
        
        # Act
        response = client.get("/api/v1/songs/1/stream")
        
        # Assert
        assert response.status_code == 200
        assert "stream_url" in response.json()["data"]
        
        app.dependency_overrides.clear()


class TestCreateSong:
    """Test create song endpoint"""
    
    def test__create_song__admin_user__creates_song(self, client, mock_song_service, mock_admin):
        # Arrange
        song = SongFactory.build()
        mock_song_service.create_song.execute.return_value = song
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"title": "New Song", "artist_id": 1, "duration": 180}
        
        # Act
        response = client.post("/api/v1/songs", json=payload)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["message"] == "Song created successfully"
        
        app.dependency_overrides.clear()
    
    def test__create_song__invalid_data__returns_422(self, client, mock_song_service, mock_admin):
        # Arrange
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"title": "", "artist_id": 1, "duration": 180}
        
        # Act
        response = client.post("/api/v1/songs", json=payload)
        
        # Assert
        assert response.status_code == 422
        
        app.dependency_overrides.clear()


class TestUpdateSong:
    """Test update song endpoint"""
    
    def test__update_song__admin_user__updates_song(self, client, mock_song_service, mock_admin):
        # Arrange
        song = SongFactory.build()
        mock_song_service.update_song.execute.return_value = song
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        payload = {"title": "Updated Song"}
        
        # Act
        response = client.put("/api/v1/songs/1", json=payload)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Song updated successfully"
        
        app.dependency_overrides.clear()


class TestDeleteSong:
    """Test delete song endpoint"""
    
    def test__delete_song__admin_user__deletes_song(self, client, mock_song_service, mock_admin):
        # Arrange
        mock_song_service.delete_song.execute.return_value = None
        
        app.dependency_overrides[get_song_service] = lambda: mock_song_service
        app.dependency_overrides[require_admin] = lambda: mock_admin
        
        # Act
        response = client.delete("/api/v1/songs/1")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Song deleted successfully"
        
        app.dependency_overrides.clear()
