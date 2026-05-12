from typing import Optional

from app.core.exceptions import NotFoundException
from app.modules.artist.repository import ArtistRepository
from app.modules.song.models import Song
from app.modules.song.repository import SongRepository
from app.modules.song.schemas import UpdateSongRequest


class UpdateSongUseCase:
    """Use case: Update song"""
    
    def __init__(self, song_repo: SongRepository, artist_repo: ArtistRepository):
        self.song_repo = song_repo
        self.artist_repo = artist_repo
    
    def execute(
        self,
        song_id: int,
        request: UpdateSongRequest,
        updated_by: Optional[str] = None
    ) -> Song:
        """
        Update song
        
        Args:
            song_id: Song ID
            request: Update data
            updated_by: Username of updater
        
        Returns:
            Updated song
        
        Raises:
            NotFoundException: If song or artist not found
        """
        # Get song
        song = self.song_repo.get_by_id(song_id)
        if not song:
            raise NotFoundException(f"Song with id {song_id} not found")
        
        # Verify artist exists if changing artist
        if request.artist_id is not None:
            artist = self.artist_repo.get_by_id(request.artist_id)
            if not artist:
                raise NotFoundException(f"Artist with id {request.artist_id} not found")
        
        # Update song
        updated_song = self.song_repo.update_song(
            song,
            title=request.title,
            artist_id=request.artist_id,
            album=request.album,
            duration=request.duration,
            thumbnail_url=str(request.thumbnail_url) if request.thumbnail_url else None,
            updated_by=updated_by
        )
        return updated_song
