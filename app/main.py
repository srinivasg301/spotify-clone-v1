from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.auth.router import router as auth_router
from app.modules.artist.router import router as artist_router
from app.modules.song.router import router as song_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Unified Spotify Clone API with modular architecture",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with /api/v1 prefix
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(artist_router, prefix="/api/v1/artists", tags=["artists"])
app.include_router(song_router, prefix="/api/v1/songs", tags=["songs"])


# Root endpoint
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "api": {
            "auth": "/api/v1/auth",
            "artists": "/api/v1/artists",
            "songs": "/api/v1/songs"
        }
    }


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
