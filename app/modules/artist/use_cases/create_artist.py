from typing import Optional

from app.modules.artist.models import Artist
from app.modules.artist.repository import ArtistRepository
from app.modules.artist.schemas import CreateArtistRequest


class CreateArtistUseCase:
    """Use case: Create new artist"""
    
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo
    
    def execute(self, request: CreateArtistRequest, created_by: Optional[str] = None) -> Artist:
        """
        Create new artist
        
        Args:
            request: Artist creation data
            created_by: Username of creator
        
        Returns:
            Created artist
        """
        artist = self.artist_repo.create(
            name=request.name,
            created_by=created_by,
            updated_by=created_by
        )
        return artist
