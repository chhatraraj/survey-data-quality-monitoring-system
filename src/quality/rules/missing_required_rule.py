from __future__ import annotations

from typing import Any, Dict, Iterable

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class MissingRequiredRule(BaseRule):
    """Checks that required fields are present."""

    def __init__(self, required_fields: Iterable[str] | None = None) -> None:
        super().__init__(name="missing_required", description="Required fields should be present")
        self.required_fields = list(required_fields or [])

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        missing = [field for field in self.required_fields if not data.get(field)]
        passed = not missing
        return RuleResult(
            passed=passed,
            rule_name=self.name,
            severity="error" if not passed else "info",
            message="All required fields are present" if passed else f"Missing required fields: {', '.join(missing)}",
            field_name="missing_fields",
            observed_value=missing,
        )
