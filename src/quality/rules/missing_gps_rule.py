"""
Validation rule for missing GPS coordinates.
"""

from src.database.models.survey_response import SurveyResponse
from src.quality.base_rule import BaseRule
from src.quality.rule_result import RuleResult
from src.utils.enums import AlertType
from src.utils.enums import SeverityLevel


class MissingGPSRule(BaseRule):
    """
    Detects survey responses that do not contain GPS coordinates.
    """

    def __init__(self):
        super().__init__(
            name="Missing GPS",
            description="Detect responses without GPS."
        )

    @property
    def rule_name(self) -> str:
        return "Missing GPS"

    def evaluate(
        self,
        response: SurveyResponse,
    ) -> RuleResult:
        """
        Validate that the survey response contains a GPS location.
        """

        if response.gps_location is None:
            return RuleResult(
                passed=False,
                rule_name=self.rule_name,
                severity=SeverityLevel.HIGH,
                observed_value=None,
                alert_type=AlertType.MISSING_GPS,
                message="Survey response does not contain GPS coordinates.",
                field_name="gps_location",
            )

        return RuleResult(
            passed=True,
            rule_name=self.rule_name,
        )