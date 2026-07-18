from __future__ import annotations

from types import SimpleNamespace

from src.quality.engine import RuleEngine
from src.quality.rule_result import RuleResult
from src.utils.enums import AlertPriority, AlertStatus, AlertType, SeverityLevel


class DummySession:
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class DummyRepository:
    def __init__(self) -> None:
        self.created: list[object] = []

    def create(self, obj: object, commit: bool = False) -> None:
        self.created.append(obj)


def test_engine_uses_result_alert_type_and_project_id() -> None:
    session = DummySession()
    quality_repository = DummyRepository()
    alert_repository = DummyRepository()
    engine = RuleEngine([], session, quality_repository, alert_repository)

    response = SimpleNamespace(response_id=42, project_id=7)
    result = RuleResult(
        passed=False,
        rule_name="Missing GPS",
        severity=SeverityLevel.HIGH,
        alert_type=AlertType.MISSING_GPS,
        message="Survey response does not contain GPS coordinates.",
    )

    engine._create_alert(response, result)

    assert len(alert_repository.created) == 1
    alert = alert_repository.created[0]
    assert alert.project_id == 7
    assert alert.response_id == 42
    assert alert.alert_type == AlertType.MISSING_GPS
    assert alert.priority == AlertPriority.HIGH
    assert alert.status == AlertStatus.OPEN
