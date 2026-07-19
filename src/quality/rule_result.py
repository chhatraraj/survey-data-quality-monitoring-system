"""
Standard result returned by every quality rule.
"""

from dataclasses import dataclass
from typing import Any

from src.utils.enums import AlertType
from src.utils.enums import SeverityLevel


@dataclass(slots=True)
class RuleResult:
    """
    Represents the outcome of a single quality rule.
    """

    passed: bool

    rule_name: str

    severity: SeverityLevel | None = None

    message: str | None = None

    field_name: str | None = None

    observed_value: Any = None

    alert_type: AlertType | None = None 