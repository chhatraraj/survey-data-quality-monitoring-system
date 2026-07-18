from __future__ import annotations

from typing import Any, Dict

from ..base_rule import BaseRule
from ..rule_result import RuleResult


class DuplicateHouseholdRule(BaseRule):
    """Checks whether a household identifier appears more than once."""

    def __init__(self) -> None:
        super().__init__(name="duplicate_household", description="Household should be unique")

    def evaluate(self, data: Dict[str, Any]) -> RuleResult:
        household_id = data.get("household_id")
        passed = household_id is not None and str(household_id).strip() != ""
        return RuleResult(
            passed=passed,
            rule_name=self.name,
            severity="warning" if not passed else "info",
            message="Household identifier is present" if passed else "Household identifier is missing",
            field_name="household_id",
            observed_value=household_id,
        )
