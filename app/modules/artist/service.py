from sqlalchemy.orm import Session

from app.modules.artist.repository import ArtistRepository
from app.modules.artist.use_cases.create_artist import CreateArtistUseCase
from app.modules.artist.use_cases.delete_artist import DeleteArtistUseCase
from app.modules.artist.use_cases.get_artist import GetArtistUseCase
from app.modules.artist.use_cases.get_artist_songs import GetArtistSongsUseCase
from app.modules.artist.use_cases.list_artists import ListArtistsUseCase
from app.modules.artist.use_cases.search_artists import SearchArtistsUseCase
from app.modules.artist.use_cases.update_artist import UpdateArtistUseCase


class ArtistService:
    """Artist service orchestrates use cases"""
    
    def __init__(self, db: Session):
        # Initialize repository
        self.artist_repo = ArtistRepository(db)
        
        # Initialize use cases
        self.create_artist = CreateArtistUseCase(self.artist_repo)
        self.update_artist = UpdateArtistUseCase(self.artist_repo)
        self.delete_artist = DeleteArtistUseCase(self.artist_repo)
        self.list_artists = ListArtistsUseCase(self.artist_repo)
        self.get_artist = GetArtistUseCase(self.artist_repo)
        self.search_artists = SearchArtistsUseCase(self.artist_repo)
        self.get_artist_songs = GetArtistSongsUseCase(self.artist_repo)
