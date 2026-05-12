from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.song.models import Song
from app.shared.base_repository import BaseRepository


class SongRepository(BaseRepository[Song]):
    """Song data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Song, db)
    
    def search_by_title(self, title: str, limit: int = 20, offset: int = 0) -> List[Song]:
        """Search songs by title (case-insensitive)"""
        return self.db.query(Song).filter(
            Song.title.ilike(f"%{title}%")
        ).limit(limit).offset(offset).all()
    
    def create_song(
        self,
        title: str,
        artist_id: int,
        duration: int,
        album: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Song:
        """Create new song"""
        song = Song(
            title=title,
            artist_id=artist_id,
            album=album,
            duration=duration,
            thumbnail_url=thumbnail_url,
            created_by=created_by,
            updated_by=created_by,
        )
        self.db.add(song)
        self.db.commit()
        self.db.refresh(song)
        return song
    
    def update_song(
        self,
        song: Song,
        title: Optional[str] = None,
        artist_id: Optional[int] = None,
        album: Optional[str] = None,
        duration: Optional[int] = None,
        thumbnail_url: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Song:
        """Update song"""
        if title is not None:
            song.title = title
        if artist_id is not None:
            song.artist_id = artist_id
        if album is not None:
            song.album = album
        if duration is not None:
            song.duration = duration
        if thumbnail_url is not None:
            song.thumbnail_url = thumbnail_url
        if updated_by is not None:
            song.updated_by = updated_by
        self.db.add(song)
        self.db.commit()
        self.db.refresh(song)
        return song
