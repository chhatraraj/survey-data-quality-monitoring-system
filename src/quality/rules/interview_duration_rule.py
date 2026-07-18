from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class InterviewDurationRule(BaseRule):
    """Checks whether the interview duration is reasonable."""

    def __init__(self) -> None:
        super().__init__(name="interview_duration", description="Interview duration should be positive")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        duration = data.get("duration")
        if duration is None:
            return RuleResult(
                passed=False,
                rule_name=self.name,
                severity="error",
                message="Duration is missing",
                field_name="duration",
                observed_value=duration,
            )

        passed = isinstance(duration, (int, float)) and duration > 0
        return RuleResult(
            passed=passed,
            rule_name=self.name,
            severity="error" if not passed else "info",
            message="Duration is valid" if passed else "Duration must be positive",
            field_name="duration",
            observed_value=duration,
        )
