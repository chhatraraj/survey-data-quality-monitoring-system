"""Repository helpers for daily progress records."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.daily_progress import DailyProgress
from src.database.repositories.base_repository import BaseRepository


class DailyProgressRepository(BaseRepository[DailyProgress]):
    """Repository for daily progress operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, DailyProgress)

    def get_by_project(self, project_id: int) -> list[DailyProgress]:
        return list(
            self.session.query(DailyProgress)
            .filter(DailyProgress.project_id == project_id)
            .all()
        )
