from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import AuditMixin, Base


class Artist(Base, AuditMixin):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)

    songs = relationship("Song", back_populates="artist", cascade="all, delete-orphan")
