from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class InvalidAgeRule(BaseRule):
    """Checks whether the respondent age is within an acceptable range."""

    def __init__(self) -> None:
        super().__init__(name="invalid_age", description="Age should be between 0 and 120")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        age = data.get("age")
        if age is None:
            return RuleResult(
                passed=False,
                rule_name=self.name,
                severity="error",
                message="Age is missing",
                field_name="age",
                observed_value=age,
            )

        passed = isinstance(age, (int, float)) and 0 <= age <= 120
        return RuleResult(
            passed=passed,
            rule_name=self.name,
            severity="error" if not passed else "info",
            message="Age is valid" if passed else "Age is outside the expected range",
            field_name="age",
            observed_value=age,
        )
