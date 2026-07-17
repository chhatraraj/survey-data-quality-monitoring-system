"""Repository helpers for anomaly scores."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.anomaly_score import AnomalyScore
from src.database.repositories.base_repository import BaseRepository


class AnomalyScoreRepository(BaseRepository[AnomalyScore]):
    """Repository for anomaly score operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, AnomalyScore)

    def get_by_response(self, response_id: int) -> list[AnomalyScore]:
        return list(
            self.session.query(AnomalyScore)
            .filter(AnomalyScore.response_id == response_id)
            .all()
        )
