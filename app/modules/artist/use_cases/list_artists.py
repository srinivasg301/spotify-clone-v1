from typing import List

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class ListArtistsUseCase:
    """Use case: List all artists"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, limit: int = 20, offset: int = 0) -> List[Artist]:
        """
        List artists with pagination
        
        Args:
            limit: Number of items per page
            offset: Starting position
        
        Returns:
            List of artists
        
        Raises:
            NotFoundException: If no artists found
        """
        artists = self.artist_repo.get_all(limit=limit, offset=offset)
        if not artists:
            raise NotFoundException("No artists found")
        logger.info("Listed %s artists (limit=%s, offset=%s)", len(artists), limit, offset)
        return artists
