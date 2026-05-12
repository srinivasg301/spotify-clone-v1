import pytest
from unittest.mock import Mock

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.use_cases.list_songs import ListSongsUseCase


@pytest.mark.unit
class TestListSongsUseCase:
    """Unit tests for ListSongsUseCase"""
    
    def test_list_songs_success(self):
        """Test successful song listing"""
        # Arrange
        mock_repo = Mock()
        mock_songs = [Song(id=1, title="Test Song", artist_id=1, duration=180)]
        mock_repo.get_all.return_value = mock_songs
        
        use_case = ListSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(limit=20, offset=0)
        
        # Assert
        assert len(songs) == 1
        assert songs[0].title == "Test Song"
        mock_repo.get_all.assert_called_once_with(limit=20, offset=0)
    
    def test_list_songs_empty(self):
        """Test listing when no songs exist"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_all.return_value = []
        
        use_case = ListSongsUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="No songs found"):
            use_case.execute(limit=20, offset=0)
    
    def test_list_songs_pagination(self):
        """Test song pagination"""
        # Arrange
        mock_repo = Mock()
        page1_songs = [Song(id=1, title="Song 0", artist_id=1, duration=180), Song(id=2, title="Song 1", artist_id=1, duration=180)]
        page2_songs = [Song(id=3, title="Song 2", artist_id=1, duration=180), Song(id=4, title="Song 3", artist_id=1, duration=180)]
        mock_repo.get_all.side_effect = [page1_songs, page2_songs]
        
        use_case = ListSongsUseCase(mock_repo)
        
        # Act
        page1 = use_case.execute(limit=2, offset=0)
        page2 = use_case.execute(limit=2, offset=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].title != page2[0].title
    
    def test_list_songs_limit(self):
        """Test song limit"""
        # Arrange
        mock_repo = Mock()
        mock_songs = [Song(id=i, title=f"Song {i}", artist_id=1, duration=180) for i in range(5)]
        mock_repo.get_all.return_value = mock_songs
        
        use_case = ListSongsUseCase(mock_repo)
        
        # Act
        songs = use_case.execute(limit=5, offset=0)
        
        # Assert
        assert len(songs) == 5
        mock_repo.get_all.assert_called_once_with(limit=5, offset=0)
