"""
Repository for QualityCheck model.

Provides database operations for rule-based
data quality validation results.
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.quality_check import QualityCheck
from src.database.repositories.base_repository import BaseRepository
from src.utils.enums import SeverityLevel


class QualityCheckRepository(BaseRepository[QualityCheck]):
    """
    Repository responsible for QualityCheck operations.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session, QualityCheck)

    # ---------------------------------------------------------
    # Filters
    # ---------------------------------------------------------

    def get_by_response(
        self,
        response_id: int,
    ) -> list[QualityCheck]:
        """
        Retrieve all quality issues for a survey response.
        """

        stmt = (
            select(QualityCheck)
            .where(QualityCheck.response_id == response_id)
            .order_by(QualityCheck.created_at)
        )

        return list(self.session.scalars(stmt))

    def get_by_rule(
        self,
        rule_name: str,
    ) -> list[QualityCheck]:
        """
        Retrieve all quality issues for a rule.
        """

        stmt = (
            select(QualityCheck)
            .where(QualityCheck.rule_name == rule_name)
            .order_by(QualityCheck.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    def get_by_severity(
        self,
        severity: SeverityLevel,
    ) -> list[QualityCheck]:
        """
        Retrieve quality issues by severity.
        """

        stmt = (
            select(QualityCheck)
            .where(QualityCheck.severity == severity)
            .order_by(QualityCheck.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    def get_critical(self) -> list[QualityCheck]:
        """
        Retrieve all critical quality issues.
        """

        stmt = (
            select(QualityCheck)
            .where(
                QualityCheck.severity == SeverityLevel.CRITICAL
            )
            .order_by(QualityCheck.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    # ---------------------------------------------------------
    # Dashboard Statistics
    # ---------------------------------------------------------

    def count_by_rule(
        self,
        rule_name: str,
    ) -> int:
        """
        Count quality issues for a rule.
        """

        stmt = (
            select(func.count())
            .select_from(QualityCheck)
            .where(QualityCheck.rule_name == rule_name)
        )

        return self.session.scalar(stmt) or 0

    def count_by_severity(
        self,
        severity: SeverityLevel,
    ) -> int:
        """
        Count quality issues by severity.
        """

        stmt = (
            select(func.count())
            .select_from(QualityCheck)
            .where(QualityCheck.severity == severity)
        )

        return self.session.scalar(stmt) or 0

    # ---------------------------------------------------------
    # Time Filters
    # ---------------------------------------------------------

    def get_recent(
        self,
        since: datetime,
    ) -> list[QualityCheck]:
        """
        Retrieve quality issues created after a given datetime.
        """

        stmt = (
            select(QualityCheck)
            .where(QualityCheck.created_at >= since)
            .order_by(QualityCheck.created_at.desc())
        )

        return list(self.session.scalars(stmt))