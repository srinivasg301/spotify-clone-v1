from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.artist.models import Artist
from app.shared.base_repository import BaseRepository


class ArtistRepository(BaseRepository[Artist]):
    """Artist data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Artist, db)
    
    def search_by_name(self, name: str, limit: int = 20, offset: int = 0) -> List[Artist]:
        """Search artists by name (case-insensitive)"""
        return self.db.query(Artist).filter(
            Artist.name.ilike(f"%{name}%")
        ).limit(limit).offset(offset).all()
    
    def get_artist_songs(self, artist_id: int, limit: int = 20, offset: int = 0):
        """Get songs for an artist"""
        from app.modules.song.models import Song
        return self.db.query(Song).filter(
            Song.artist_id == artist_id
        ).limit(limit).offset(offset).all()
