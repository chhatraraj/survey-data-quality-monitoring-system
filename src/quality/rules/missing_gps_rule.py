from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class MissingGPSRule(BaseRule):
    """Ensures GPS data is present for a response."""

    def __init__(self) -> None:
        super().__init__(name="missing_gps", description="GPS coordinates are required")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        lat = data.get("latitude")
        lon = data.get("longitude")
        passed = lat is not None and lon is not None
        return RuleResult(
            passed=passed,
            message="GPS coordinates are missing" if not passed else "GPS coordinates are present",
            details={"latitude": lat, "longitude": lon},
            rule_name=self.name,
            severity="error" if not passed else "info",
        )
