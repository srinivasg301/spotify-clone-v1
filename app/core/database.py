from datetime import datetime
from typing import Generator

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


# Database engine
engine = create_engine(settings.database_url, echo=settings.debug)

# Session factory
SessionLocal = sessionmaker(bind=engine, class_=Session, autocommit=False, autoflush=False)


# Base model for all tables
class Base(DeclarativeBase):
    pass


# Audit mixin for created/updated tracking
class AuditMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
