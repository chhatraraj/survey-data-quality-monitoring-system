from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from .base_rule import BaseRule
from .rule_result import RuleResult


class RuleEngine:
    """Simple engine that runs a collection of quality rules."""

    def __init__(self, rules: Optional[Sequence[BaseRule]] = None) -> None:
        self.rules = list(rules or [])

    def add_rule(self, rule: BaseRule) -> None:
        self.rules.append(rule)

    def run(self, data: Dict[str, Any]) -> List[RuleResult]:
        return [rule.evaluate(data) for rule in self.rules]
