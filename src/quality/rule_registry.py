"""
Registry for all quality validation rules.

This module centralizes rule registration so that
new rules can be added in one place.
"""

from src.quality.base_rule import BaseRule
from src.quality.rules.missing_gps_rule import MissingGPSRule


def get_rules() -> list[BaseRule]:
    """
    Return all enabled quality rules.
    """

    return [
        MissingGPSRule(),
    ]