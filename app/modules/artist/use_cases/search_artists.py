from typing import List

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class SearchArtistsUseCase:
    """Use case: Search artists by name"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, name: str, limit: int = 20, offset: int = 0) -> List[Artist]:
        """
        Search artists by name
        
        Args:
            name: Search query
            limit: Number of items per page
            offset: Starting position
        
        Returns:
            List of matching artists
        
        Raises:
            NotFoundException: If no artists found
        """
        artists = self.artist_repo.search_by_name(name, limit=limit, offset=offset)
        if not artists:
            raise NotFoundException(f"No artists found matching '{name}'")
        logger.info("Artist search: query='%s', results=%s", name, len(artists))
        return artists
