"""
Repository for Alert model.

Provides database operations for system alerts.
"""

from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.alert import Alert
from src.database.repositories.base_repository import BaseRepository
from src.utils.enums import AlertPriority
from src.utils.enums import AlertStatus


class AlertRepository(BaseRepository[Alert]):
    """
    Repository responsible for Alert database operations.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session, Alert)

    # ---------------------------------------------------------
    # Filters
    # ---------------------------------------------------------

    def get_by_priority(
        self,
        priority: AlertPriority,
    ) -> list[Alert]:
        """
        Retrieve alerts by priority.
        """

        stmt = (
            select(Alert)
            .where(Alert.priority == priority)
            .order_by(Alert.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    def get_by_status(
        self,
        status: AlertStatus,
    ) -> list[Alert]:
        """
        Retrieve alerts by status.
        """

        stmt = (
            select(Alert)
            .where(Alert.status == status)
            .order_by(Alert.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    def get_by_type(
        self,
        alert_type: str,
    ) -> list[Alert]:
        """
        Retrieve alerts by type.
        """

        stmt = (
            select(Alert)
            .where(Alert.alert_type == alert_type)
            .order_by(Alert.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    def get_open_alerts(self) -> list[Alert]:
        """
        Retrieve all open alerts.
        """

        stmt = (
            select(Alert)
            .where(Alert.status == AlertStatus.OPEN)
            .order_by(
                Alert.priority.desc(),
                Alert.created_at.desc()
            )
        )

        return list(self.session.scalars(stmt))

    def get_unresolved(self) -> list[Alert]:
        """
        Retrieve alerts that have not been resolved.
        """

        stmt = (
            select(Alert)
            .where(Alert.status != AlertStatus.RESOLVED)
            .order_by(Alert.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_open(self) -> int:
        """
        Count open alerts.
        """

        stmt = (
            select(func.count())
            .select_from(Alert)
            .where(Alert.status == AlertStatus.OPEN)
        )

        return self.session.scalar(stmt) or 0

    def count_by_priority(
        self,
        priority: AlertPriority,
    ) -> int:
        """
        Count alerts by priority.
        """

        stmt = (
            select(func.count())
            .select_from(Alert)
            .where(Alert.priority == priority)
        )

        return self.session.scalar(stmt) or 0

    # ---------------------------------------------------------
    # Time Filters
    # ---------------------------------------------------------

    def get_recent(
        self,
        since: datetime,
    ) -> list[Alert]:
        """
        Retrieve alerts created after a specific datetime.
        """

        stmt = (
            select(Alert)
            .where(Alert.created_at >= since)
            .order_by(Alert.created_at.desc())
        )

        return list(self.session.scalars(stmt))

    # ---------------------------------------------------------
    # Alert Management
    # ---------------------------------------------------------

    def resolve_alert(
        self,
        alert: Alert,
    ) -> Alert:
        """
        Mark an alert as resolved.
        """

        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now(UTC)

        self.session.commit()
        self.session.refresh(alert)

        return alert