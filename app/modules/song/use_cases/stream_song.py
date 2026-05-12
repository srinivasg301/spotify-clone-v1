from app.core.exceptions import NotFoundException
from app.modules.song.repository import SongRepository
from app.modules.song.schemas import SongStreamResponse


class StreamSongUseCase:
    """Use case: Get song stream URL"""
    
    def __init__(self, song_repo: SongRepository):
        self.song_repo = song_repo
    
    def execute(self, song_id: int) -> SongStreamResponse:
        """
        Get stream URL for song
        
        Args:
            song_id: Song ID
        
        Returns:
            Song stream response with URL
        
        Raises:
            NotFoundException: If song not found
        """
        song = self.song_repo.get_by_id(song_id)
        if not song:
            raise NotFoundException(f"Song with id {song_id} not found")
        
        # Generate stream URL (in production, this would be a CDN URL)
        stream_url = f"https://cdn.spotify-clone.com/stream/{song.id}"
        
        return SongStreamResponse(
            id=song.id,
            title=song.title,
            stream_url=stream_url
        )
