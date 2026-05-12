from app.core.exceptions import NotFoundException
from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository


class GetArtistUseCase:
    """Use case: Get artist by ID"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, artist_id: int) -> Artist:
        """
        Get artist by ID
        
        Args:
            artist_id: Artist ID
        
        Returns:
            Artist
        
        Raises:
            NotFoundException: If artist not found
        """
        artist = self.artist_repo.get_by_id(artist_id)
        if not artist:
            raise NotFoundException(f"Artist with id {artist_id} not found")
        return artist
