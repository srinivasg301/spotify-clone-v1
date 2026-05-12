from typing import Optional

from app.core.exceptions import NotFoundException
from app.modules.artist.repository import ArtistRepository
from app.modules.song.models import Song
from app.modules.song.repository import SongRepository
from app.modules.song.schemas import CreateSongRequest
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateSongUseCase:
    """Use case: Create new song"""
    
    def __init__(self, song_repo: SongRepository, artist_repo: ArtistRepository):
        self.song_repo = song_repo
        self.artist_repo = artist_repo
    
    def execute(self, request: CreateSongRequest, created_by: Optional[str] = None) -> Song:
        """
        Create new song
        
        Args:
            request: Song creation data
            created_by: Username of creator
        
        Returns:
            Created song
        
        Raises:
            NotFoundException: If artist not found
        """
        # Verify artist exists
        artist = self.artist_repo.get_by_id(request.artist_id)
        if not artist:
            raise NotFoundException(f"Artist with id {request.artist_id} not found")
        
        # Create song
        song = self.song_repo.create_song(
            title=request.title,
            artist_id=request.artist_id,
            album=request.album,
            duration=request.duration,
            thumbnail_url=str(request.thumbnail_url) if request.thumbnail_url else None,
            created_by=created_by
        )
        logger.info("Song created: id=%s, title=%s, by=%s", song.id, song.title, created_by)
        return song
