
"""
Rule Engine.

Runs quality rules against survey responses.
"""

from sqlalchemy.orm import Session

from src.database.models.alert import Alert
from src.database.models.quality_check import QualityCheck
from src.database.models.survey_response import SurveyResponse

from src.database.repositories.alert_repository import AlertRepository
from src.database.repositories.quality_check_repository import (
    QualityCheckRepository,
)

from src.quality.base_rule import BaseRule
from src.quality.rule_result import RuleResult

from src.utils.enums import (
    AlertPriority,
    AlertStatus,
    AlertType,
    SeverityLevel,
)


class RuleEngine:
    """Executes quality validation rules."""

    def __init__(
        self,
        rules: list[BaseRule],
        session: Session,
        quality_repository: QualityCheckRepository,
        alert_repository: AlertRepository,
    ) -> None:
        self.rules = rules
        self.session = session
        self.quality_repository = quality_repository
        self.alert_repository = alert_repository

    def process(self, response: SurveyResponse) -> list[RuleResult]:
        results: list[RuleResult] = []

        try:
            for rule in self.rules:
                result = rule.evaluate(response)
                results.append(result)

                if result.passed:
                    continue

                self._save_quality_check(response, result)

                if self._should_create_alert(result):
                    self._create_alert(response, result)

            self.session.commit()
            return results

        except Exception:
            self.session.rollback()
            raise

    def _save_quality_check(
        self,
        response: SurveyResponse,
        result: RuleResult,
    ) -> None:
        severity = self._normalize_severity(result.severity)
        quality_check = QualityCheck(
            response_id=response.response_id,
            rule_name=result.rule_name,
            severity=severity,
            message=result.message,
        )

        self.quality_repository.create(quality_check, commit=False)

    def _create_alert(
        self,
        response: SurveyResponse,
        result: RuleResult,
    ) -> None:
        severity = self._normalize_severity(result.severity)
        alert = Alert(
            response_id=response.response_id,
            project_id=response.project_id,
            alert_type=self._normalize_alert_type(result.rule_name),
            priority=AlertPriority[severity.name],
            status=AlertStatus.OPEN,
            message=result.message,
        )

        self.alert_repository.create(alert, commit=False)

    def _should_create_alert(self, result: RuleResult) -> bool:
        severity = self._normalize_severity(result.severity)
        return severity in (SeverityLevel.HIGH, SeverityLevel.CRITICAL)

    def _normalize_severity(self, severity: object) -> SeverityLevel:
        if isinstance(severity, SeverityLevel):
            return severity

        if isinstance(severity, str):
            value = severity.strip().upper()
            if value in SeverityLevel.__members__:
                return SeverityLevel[value]
            if value in {"ERROR", "WARNING", "INFO"}:
                if value == "ERROR":
                    return SeverityLevel.CRITICAL
                if value == "WARNING":
                    return SeverityLevel.MEDIUM
                return SeverityLevel.LOW

        return SeverityLevel.MEDIUM

    def _normalize_alert_type(self, rule_name: str | None) -> AlertType:
        if not rule_name:
            return AlertType.ML_ANOMALY

        normalized = rule_name.strip().lower().replace("-", "_")

        mapping = {
            "missing_gps": AlertType.MISSING_GPS,
            "duplicate_household": AlertType.DUPLICATE_HOUSEHOLD,
            "duplicate_device": AlertType.DUPLICATE_DEVICE,
            "geofence": AlertType.OUTSIDE_GEOFENCE,
            "invalid_age": AlertType.ML_ANOMALY,
            "interview_duration": AlertType.SPEEDER,
            "missing_required": AlertType.ML_ANOMALY,
        }

        return mapping.get(normalized, AlertType.ML_ANOMALY)

   