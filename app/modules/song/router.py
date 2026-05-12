from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user, require_admin
from app.modules.song.schemas import (
    CreateSongRequest,
    SongResponse,
    SongStreamResponse,
    UpdateSongRequest,
)
from app.modules.song.service import SongService
from app.shared.base_schema import SuccessResponse

router = APIRouter(tags=["songs"])


def get_song_service(db: Session = Depends(get_db)) -> SongService:
    """Dependency to get song service"""
    return SongService(db)


@router.get("", response_model=SuccessResponse[List[SongResponse]])
def list_songs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[List[SongResponse]]:
    """List all songs"""
    songs = service.list_songs.execute(limit=limit, offset=offset)
    return SuccessResponse(
        data=[SongResponse.model_validate(s) for s in songs]
    )


@router.get("/search", response_model=SuccessResponse[List[SongResponse]])
def search_songs(
    title: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[List[SongResponse]]:
    """Search songs by title"""
    songs = service.search_songs.execute(title=title, limit=limit, offset=offset)
    return SuccessResponse(
        data=[SongResponse.model_validate(s) for s in songs]
    )


@router.get("/{song_id}", response_model=SuccessResponse[SongResponse])
def get_song(
    song_id: int,
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[SongResponse]:
    """Get song by ID"""
    song = service.get_song.execute(song_id)
    return SuccessResponse(data=SongResponse.model_validate(song))


@router.get("/{song_id}/stream", response_model=SuccessResponse[SongStreamResponse])
def stream_song(
    song_id: int,
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[SongStreamResponse]:
    """Get song stream URL"""
    stream = service.stream_song.execute(song_id)
    return SuccessResponse(data=stream)


@router.post("", response_model=SuccessResponse[SongResponse], status_code=201)
def create_song(
    request: CreateSongRequest,
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[SongResponse]:
    """Create new song (admin only)"""
    song = service.create_song.execute(request, created_by=user.username)
    return SuccessResponse(
        data=SongResponse.model_validate(song),
        message="Song created successfully"
    )


@router.put("/{song_id}", response_model=SuccessResponse[SongResponse])
def update_song(
    song_id: int,
    request: UpdateSongRequest,
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[SongResponse]:
    """Update song (admin only)"""
    song = service.update_song.execute(song_id, request, updated_by=user.username)
    return SuccessResponse(
        data=SongResponse.model_validate(song),
        message="Song updated successfully"
    )


@router.delete("/{song_id}", response_model=SuccessResponse[None])
def delete_song(
    song_id: int,
    service: SongService = Depends(get_song_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[None]:
    """Delete song (admin only)"""
    service.delete_song.execute(song_id)
    return SuccessResponse(data=None, message="Song deleted successfully")
