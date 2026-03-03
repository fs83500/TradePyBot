"""
CRUD operations for database
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import TypeVar, Generic, List, Optional, Type
from datetime import datetime

T = TypeVar('T')


class CRUD:
    """Base CRUD operations"""
    
    @staticmethod
    async def create(db: AsyncSession, model: T) -> T:
        """Create a new record"""
        db.add(model)
        await db.commit()
        await db.refresh(model)
        return model
    
    @staticmethod
    async def get_by_id(db: AsyncSession, model_class: Type[T], id: int) -> Optional[T]:
        """Get record by ID"""
        result = await db.execute(select(model_class).where(model_class.id == id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_field(db: AsyncSession, model_class: Type[T], field: str, value) -> Optional[T]:
        """Get record by field value"""
        result = await db.execute(select(model_class).where(getattr(model_class, field) == value))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db: AsyncSession, model_class: Type[T]) -> List[T]:
        """Get all records"""
        result = await db.execute(select(model_class))
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, model: T, **kwargs) -> T:
        """Update record fields"""
        for key, value in kwargs.items():
            setattr(model, key, value)
        await db.commit()
        await db.refresh(model)
        return model
    
    @staticmethod
    async def delete(db: AsyncSession, model: T) -> None:
        """Delete record"""
        await db.delete(model)
        await db.commit()
