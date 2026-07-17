"""Repository helpers for quality checks."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.quality_check import QualityCheck
from src.database.repositories.base_repository import BaseRepository


class QualityCheckRepository(BaseRepository[QualityCheck]):
    """Repository for quality check operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, QualityCheck)

    def get_by_response(self, response_id: int) -> list[QualityCheck]:
        return list(
            self.session.query(QualityCheck)
            .filter(QualityCheck.response_id == response_id)
            .all()
        )
