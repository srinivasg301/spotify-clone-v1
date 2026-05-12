from typing import Optional

from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from app.modules.artist.schemas import UpdateArtistRequest
from app.core.logger import get_logger

logger = get_logger(__name__)


class UpdateArtistUseCase:
    """Use case: Update artist"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(
        self,
        artist_id: int,
        request: UpdateArtistRequest,
        updated_by: Optional[str] = None
    ) -> Artist:
        """
        Update artist
        
        Args:
            artist_id: Artist ID
            request: Update data
            updated_by: Username of updater
        
        Returns:
            Updated artist
        
        Raises:
            NotFoundException: If artist not found
        """
        artist = self.artist_repo.get_by_id(artist_id)
        if not artist:
            raise NotFoundException(f"Artist with id {artist_id} not found")
        
        updated_artist = self.artist_repo.update(
            artist,
            name=request.name,
            updated_by=updated_by
        )
        logger.info("Artist updated: id=%s, by=%s", artist_id, updated_by)
        return updated_artist
