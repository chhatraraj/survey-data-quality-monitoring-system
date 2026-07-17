"""Repository helpers for survey responses."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.survey_response import SurveyResponse
from src.database.repositories.base_repository import BaseRepository


class SurveyResponseRepository(BaseRepository[SurveyResponse]):
    """Repository for survey response operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, SurveyResponse)

    def get_by_project(self, project_id: int) -> list[SurveyResponse]:
        return list(
            self.session.query(SurveyResponse)
            .filter(SurveyResponse.project_id == project_id)
            .all()
        )

    def get_by_enumerator(self, enumerator_id: int) -> list[SurveyResponse]:
        return list(
            self.session.query(SurveyResponse)
            .filter(SurveyResponse.enumerator_id == enumerator_id)
            .all()
        )
