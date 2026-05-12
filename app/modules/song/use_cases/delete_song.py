from app.core.exceptions import NotFoundException
from app.modules.song.repository import SongRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class DeleteSongUseCase:
    """Use case: Delete song"""
    
    def __init__(self, song_repo: SongRepository):
        self.song_repo = song_repo
    
    def execute(self, song_id: int) -> None:
        """
        Delete song
        
        Args:
            song_id: Song ID
        
        Raises:
            NotFoundException: If song not found
        """
        song = self.song_repo.get_by_id(song_id)
        if not song:
            raise NotFoundException(f"Song with id {song_id} not found")
        
        self.song_repo.delete(song)
        logger.info("Song deleted: id=%s", song_id)
