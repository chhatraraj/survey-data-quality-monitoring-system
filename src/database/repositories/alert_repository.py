"""Repository helpers for alerts."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.alert import Alert
from src.database.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    """Repository for alert-related operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, Alert)

    def get_by_project(self, project_id: int) -> list[Alert]:
        return list(
            self.session.query(Alert)
            .filter(Alert.project_id == project_id)
            .all()
        )

    def get_open_alerts(self) -> list[Alert]:
        return list(
            self.session.query(Alert)
            .filter(Alert.status == "Open")
            .all()
        )
