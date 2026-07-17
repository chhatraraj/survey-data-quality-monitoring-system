"""Repository helpers for survey forms."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.survey_form import SurveyForm
from src.database.repositories.base_repository import BaseRepository


class SurveyFormRepository(BaseRepository[SurveyForm]):
    """Repository for survey form operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, SurveyForm)

    def get_by_project(self, project_id: int) -> list[SurveyForm]:
        return list(
            self.session.query(SurveyForm)
            .filter(SurveyForm.project_id == project_id)
            .all()
        )
