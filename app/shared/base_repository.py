from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.core.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, limit: int = 20, offset: int = 0) -> List[ModelType]:
        """Get all records with pagination"""
        return self.db.query(self.model).limit(limit).offset(offset).all()
    
    def create(self, **kwargs) -> ModelType:
        """Create new record"""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Update existing record"""
        for key, value in kwargs.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def delete(self, instance: ModelType) -> None:
        """Delete record"""
        self.db.delete(instance)
        self.db.commit()
    
    def count(self) -> int:
        """Count total records"""
        return self.db.query(self.model).count()
