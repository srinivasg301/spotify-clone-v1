from app.core.exceptions import NotFoundException
from app.modules.artist.repository import ArtistRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class DeleteArtistUseCase:
    """Use case: Delete artist"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, artist_id: int) -> None:
        """
        Delete artist
        
        Args:
            artist_id: Artist ID
        
        Raises:
            NotFoundException: If artist not found
        """
        artist = self.artist_repo.get_by_id(artist_id)
        if not artist:
            raise NotFoundException(f"Artist with id {artist_id} not found")
        
        self.artist_repo.delete(artist)
        logger.info("Artist deleted: id=%s", artist_id)
