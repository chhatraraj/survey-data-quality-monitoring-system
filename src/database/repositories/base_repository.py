"""
Base Repository

Provides reusable CRUD operations for all ORM models.
"""

from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from src.database.base import Base

# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(self, session: Session, model: type[ModelType]):
        self.session = session
        self.model = model

    def create(
        self,
        entity: ModelType,
        commit: bool = True,
    ) -> ModelType:
        self.session.add(entity)

        if commit:
            self.session.commit()
            self.session.refresh(entity)

        return entity

    def get(self, obj_id: int) -> ModelType | None:
        return self.session.get(self.model, obj_id)

    def get_all(self) -> list[ModelType]:
        return self.session.query(self.model).all()

    def update(self, obj: ModelType) -> None:
        self.session.commit()

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
        self.session.commit()