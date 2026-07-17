"""
Repository for SurveyResponse model.

Provides survey response specific database operations.
"""

from datetime import date
from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.survey_response import SurveyResponse
from src.database.repositories.base_repository import BaseRepository


class SurveyResponseRepository(BaseRepository[SurveyResponse]):
    """
    Repository responsible for SurveyResponse operations.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session, SurveyResponse)

    # --------------------------------------------------------
    # Basic Filters
    # --------------------------------------------------------

    def get_by_project(
        self,
        project_id: int,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(SurveyResponse.project_id == project_id)
            .order_by(SurveyResponse.submission_time)
        )

        return list(self.session.scalars(stmt))

    def get_by_form(
        self,
        form_id: int,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(SurveyResponse.form_id == form_id)
        )

        return list(self.session.scalars(stmt))

    def get_by_enumerator(
        self,
        enumerator_id: int,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.enumerator_id == enumerator_id
            )
            .order_by(SurveyResponse.submission_time)
        )

        return list(self.session.scalars(stmt))

    # --------------------------------------------------------
    # Date Filters
    # --------------------------------------------------------

    def get_today(self) -> list[SurveyResponse]:

        today = date.today()

        stmt = (
            select(SurveyResponse)
            .where(
                func.date(
                    SurveyResponse.submission_time
                ) == today
            )
        )

        return list(self.session.scalars(stmt))

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.submission_time.between(
                    start_date,
                    end_date,
                )
            )
            .order_by(SurveyResponse.submission_time)
        )

        return list(self.session.scalars(stmt))

    # --------------------------------------------------------
    # Quality Checks
    # --------------------------------------------------------

    def get_missing_gps(self) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.location.is_(None)
            )
        )

        return list(self.session.scalars(stmt))

    def get_invalid_age(self) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.respondent_age > 120
            )
        )

        return list(self.session.scalars(stmt))

    def get_by_household(
        self,
        household_id: str,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.household_id == household_id
            )
        )

        return list(self.session.scalars(stmt))

    def get_by_device(
        self,
        device_id: str,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.device_id == device_id
            )
        )

        return list(self.session.scalars(stmt))

    def get_by_district(
        self,
        district: str,
    ) -> list[SurveyResponse]:

        stmt = (
            select(SurveyResponse)
            .where(
                SurveyResponse.district == district
            )
        )

        return list(self.session.scalars(stmt))

    # --------------------------------------------------------
    # Dashboard Statistics
    # --------------------------------------------------------

    def get_completed_today_count(self) -> int:

        today = date.today()

        stmt = (
            select(func.count())
            .select_from(SurveyResponse)
            .where(
                func.date(
                    SurveyResponse.submission_time
                ) == today
            )
        )

        return self.session.scalar(stmt) or 0

    def get_average_duration(self) -> float:

        stmt = (
            select(
                func.avg(
                    SurveyResponse.interview_duration_seconds
                )
            )
        )

        result = self.session.scalar(stmt)

        return float(result or 0)