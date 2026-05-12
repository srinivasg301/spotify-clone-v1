from app.core.exceptions import NotFoundException
from app.modules.song.models import Song
from app.modules.song.repository import SongRepository


class GetSongUseCase:
    """Use case: Get song by ID"""
    
    def __init__(self, song_repo: SongRepository):
        self.song_repo = song_repo
    
    def execute(self, song_id: int) -> Song:
        """
        Get song by ID
        
        Args:
            song_id: Song ID
        
        Returns:
            Song
        
        Raises:
            NotFoundException: If song not found
        """
        song = self.song_repo.get_by_id(song_id)
        if not song:
            raise NotFoundException(f"Song with id {song_id} not found")
        return song
