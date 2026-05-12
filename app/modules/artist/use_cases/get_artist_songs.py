from typing import List

from app.core.exceptions import NotFoundException
from app.modules.artist.repository import ArtistRepository


class GetArtistSongsUseCase:
    """Use case: Get songs by artist"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, artist_id: int, limit: int = 20, offset: int = 0) -> List:
        """
        Get songs for an artist
        
        Args:
            artist_id: Artist ID
            limit: Number of items per page
            offset: Starting position
        
        Returns:
            List of songs
        
        Raises:
            NotFoundException: If artist not found or no songs found
        """
        # Check if artist exists
        artist = self.artist_repo.get_by_id(artist_id)
        if not artist:
            raise NotFoundException(f"Artist with id {artist_id} not found")
        
        # Get artist's songs
        songs = self.artist_repo.get_artist_songs(artist_id, limit=limit, offset=offset)
        if not songs:
            raise NotFoundException(f"No songs found for artist '{artist.name}'")
        
        return songs
