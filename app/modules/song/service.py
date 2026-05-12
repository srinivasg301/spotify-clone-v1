from sqlalchemy.orm import Session

from app.modules.artist.repository import ArtistRepository
from app.modules.song.repository import SongRepository
from app.modules.song.use_cases.create_song import CreateSongUseCase
from app.modules.song.use_cases.delete_song import DeleteSongUseCase
from app.modules.song.use_cases.get_song import GetSongUseCase
from app.modules.song.use_cases.list_songs import ListSongsUseCase
from app.modules.song.use_cases.search_songs import SearchSongsUseCase
from app.modules.song.use_cases.stream_song import StreamSongUseCase
from app.modules.song.use_cases.update_song import UpdateSongUseCase


class SongService:
    """Song service orchestrates use cases"""
    
    def __init__(self, db: Session):
        # Initialize repositories
        self.song_repo = SongRepository(db)
        self.artist_repo = ArtistRepository(db)
        
        # Initialize use cases
        self.create_song = CreateSongUseCase(self.song_repo, self.artist_repo)
        self.update_song = UpdateSongUseCase(self.song_repo, self.artist_repo)
        self.delete_song = DeleteSongUseCase(self.song_repo)
        self.list_songs = ListSongsUseCase(self.song_repo)
        self.get_song = GetSongUseCase(self.song_repo)
        self.search_songs = SearchSongsUseCase(self.song_repo)
        self.stream_song = StreamSongUseCase(self.song_repo)
