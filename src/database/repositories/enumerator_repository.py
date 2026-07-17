"""Repository helpers for enumerators."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.enumerator import Enumerator
from src.database.repositories.base_repository import BaseRepository


class EnumeratorRepository(BaseRepository[Enumerator]):
    """Repository for enumerator operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, Enumerator)

    def get_by_project(self, project_id: int) -> list[Enumerator]:
        return list(
            self.session.query(Enumerator)
            .filter(Enumerator.project_id == project_id)
            .all()
        )
