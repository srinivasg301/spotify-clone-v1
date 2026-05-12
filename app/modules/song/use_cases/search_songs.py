from typing import List

from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.repository import SongRepository


class SearchSongsUseCase:
    """Use case: Search songs by title"""
    
    def __init__(self, song_repo: SongRepository):
        self.song_repo = song_repo
    
    def execute(self, title: str, limit: int = 20, offset: int = 0) -> List[Song]:
        """
        Search songs by title
        
        Args:
            title: Search query
            limit: Number of items per page
            offset: Starting position
        
        Returns:
            List of matching songs
        
        Raises:
            NotFoundException: If no songs found
        """
        songs = self.song_repo.search_by_title(title, limit=limit, offset=offset)
        if not songs:
            raise NotFoundException(f"No songs found matching '{title}'")
        return songs
