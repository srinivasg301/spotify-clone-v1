from typing import List

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.repository import SongRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class ListSongsUseCase:
    """Use case: List all songs"""
    
    def __init__(self, song_repo: SongRepository):
        self.song_repo = song_repo
    
    def execute(self, limit: int = 20, offset: int = 0) -> List[Song]:
        """
        List songs with pagination
        
        Args:
            limit: Number of items per page
            offset: Starting position
        
        Returns:
            List of songs
        
        Raises:
            NotFoundException: If no songs found
        """
        songs = self.song_repo.get_all(limit=limit, offset=offset)
        if not songs:
            raise NotFoundException("No songs found")
        logger.info("Listed %s songs (limit=%s, offset=%s)", len(songs), limit, offset)
        return songs
