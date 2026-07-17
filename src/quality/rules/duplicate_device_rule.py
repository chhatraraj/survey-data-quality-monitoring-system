from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class DuplicateDeviceRule(BaseRule):
    """Checks whether a device identifier is present and unique."""

    def __init__(self) -> None:
        super().__init__(name="duplicate_device", description="Device identifier should be unique")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        device_id = data.get("device_id")
        passed = device_id is not None and str(device_id).strip() != ""
        return RuleResult(
            passed=passed,
            message="Device identifier is present" if passed else "Device identifier is missing",
            details={"device_id": device_id},
            rule_name=self.name,
            severity="warning" if not passed else "info",
        )
