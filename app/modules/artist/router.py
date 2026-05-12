from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user, require_admin
from app.modules.artist.schemas import ArtistResponse, CreateArtistRequest, UpdateArtistRequest
from app.modules.artist.service import ArtistService
from app.shared.base_schema import SuccessResponse

router = APIRouter(tags=["artists"])


def get_artist_service(db: Session = Depends(get_db)) -> ArtistService:
    """Dependency to get artist service"""
    return ArtistService(db)


@router.get("", response_model=SuccessResponse[List[ArtistResponse]])
def list_artists(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[List[ArtistResponse]]:
    """List all artists"""
    artists = service.list_artists.execute(limit=limit, offset=offset)
    return SuccessResponse(
        data=[ArtistResponse.model_validate(a) for a in artists]
    )


@router.get("/search", response_model=SuccessResponse[List[ArtistResponse]])
def search_artists(
    name: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[List[ArtistResponse]]:
    """Search artists by name"""
    artists = service.search_artists.execute(name=name, limit=limit, offset=offset)
    return SuccessResponse(
        data=[ArtistResponse.model_validate(a) for a in artists]
    )


@router.get("/{artist_id}", response_model=SuccessResponse[ArtistResponse])
def get_artist(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[ArtistResponse]:
    """Get artist by ID"""
    artist = service.get_artist.execute(artist_id)
    return SuccessResponse(data=ArtistResponse.model_validate(artist))


@router.get("/{artist_id}/songs", response_model=SuccessResponse[List])
def get_artist_songs(
    artist_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(get_current_user),
) -> SuccessResponse[List]:
    """Get songs by artist"""
    from app.modules.song.schemas import SongResponse
    
    songs = service.get_artist_songs.execute(artist_id=artist_id, limit=limit, offset=offset)
    return SuccessResponse(
        data=[SongResponse.model_validate(s) for s in songs]
    )


@router.post("", response_model=SuccessResponse[ArtistResponse], status_code=201)
def create_artist(
    request: CreateArtistRequest,
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[ArtistResponse]:
    """Create new artist (admin only)"""
    artist = service.create_artist.execute(request, created_by=user.username)
    return SuccessResponse(
        data=ArtistResponse.model_validate(artist),
        message="Artist created successfully"
    )


@router.put("/{artist_id}", response_model=SuccessResponse[ArtistResponse])
def update_artist(
    artist_id: int,
    request: UpdateArtistRequest,
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[ArtistResponse]:
    """Update artist (admin only)"""
    artist = service.update_artist.execute(artist_id, request, updated_by=user.username)
    return SuccessResponse(
        data=ArtistResponse.model_validate(artist),
        message="Artist updated successfully"
    )


@router.delete("/{artist_id}", response_model=SuccessResponse[None])
def delete_artist(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service),
    user: UserContext = Depends(require_admin),
) -> SuccessResponse[None]:
    """Delete artist (admin only)"""
    service.delete_artist.execute(artist_id)
    return SuccessResponse(data=None, message="Artist deleted successfully")
