"""
Application dependency wiring.

Creates reusable application services.
"""

from sqlalchemy.orm import Session

from src.database.repositories.alert_repository import AlertRepository
from src.database.repositories.quality_check_repository import (
    QualityCheckRepository,
)
from src.quality.engine import RuleEngine
from src.quality.rule_registry import get_rules
from src.services.quality_service import QualityService


def create_quality_service(session: Session) -> QualityService:
    """
    Create a fully configured QualityService.
    """

    quality_repository = QualityCheckRepository(session)

    alert_repository = AlertRepository(session)

    engine = RuleEngine(
        rules=get_rules(),
        session=session,
        quality_repository=quality_repository,
        alert_repository=alert_repository,
    )

    return QualityService(engine)