from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class GeofenceRule(BaseRule):
    """Placeholder geofence validation rule."""

    def __init__(self) -> None:
        super().__init__(name="geofence", description="Respondent must be inside the allowed area")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        passed = True
        return RuleResult(
            passed=passed,
            message="Geofence check passed",
            details=data,
            rule_name=self.name,
            severity="info",
        )
