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
            return RuleResult(False, "Duration is missing", {"duration": duration}, self.name, "error")

        passed = isinstance(duration, (int, float)) and duration > 0
        return RuleResult(
            passed=passed,
            message="Duration is valid" if passed else "Duration must be positive",
            details={"duration": duration},
            rule_name=self.name,
            severity="error" if not passed else "info",
        )
