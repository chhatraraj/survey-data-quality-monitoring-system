"""
Base Repository

Provides reusable CRUD operations for all ORM models.
"""

from __future__ import annotations

from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.base import Base

# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository providing reusable CRUD operations.
    """

    def __init__(
        self,
        session: Session,
        model: type[ModelType],
    ) -> None:
        self.session = session
        self.model = model

    def create(
        self,
        entity: ModelType,
        commit: bool = True,
    ) -> ModelType:
        """
        Persist a new entity.
        """

        self.session.add(entity)

        if commit:
            self.session.commit()
            self.session.refresh(entity)

        return entity

    def get(
        self,
        obj_id: int,
    ) -> ModelType | None:
        """
        Retrieve an entity by primary key.
        """

        return self.session.get(self.model, obj_id)

    def get_all(self) -> list[ModelType]:
        """
        Retrieve all records.
        """

        return list(
            self.session.scalars(
                select(self.model)
            )
        )

    def get_by_field(
        self,
        field_name: str,
        value: Any,
    ) -> ModelType | None:
        """
        Retrieve the first record matching a field.
        """

        field = getattr(self.model, field_name)

        statement = (
            select(self.model)
            .where(field == value)
        )

        return self.session.scalar(statement)

    def exists(
        self,
        field_name: str,
        value: Any,
    ) -> bool:
        """
        Check whether a record exists.
        """

        return (
            self.get_by_field(
                field_name,
                value,
            )
            is not None
        )

    def update(
        self,
        entity: ModelType,
        commit: bool = True,
    ) -> ModelType:
        """
        Update an existing entity.
        """

        if commit:
            self.session.commit()
            self.session.refresh(entity)

        return entity

    def delete(
        self,
        entity: ModelType,
        commit: bool = True,
    ) -> None:
        """
        Delete an entity.
        """

        self.session.delete(entity)

        if commit:
            self.session.commit()