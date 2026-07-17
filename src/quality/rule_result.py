"""
Main Rule Engine.

Executes all registered quality rules against
a survey response.
"""

from src.database.models.survey_response import SurveyResponse
from src.quality.base_rule import BaseRule
from src.quality.rule_result import RuleResult


class RuleEngine:
    """
    Executes quality validation rules.
    """

    def __init__(
        self,
        rules: list[BaseRule],
    ) -> None:
        """
        Parameters
        ----------
        rules
            List of validation rules.
        """

        self.rules = rules

    def evaluate(
        self,
        response: SurveyResponse,
    ) -> list[RuleResult]:
        """
        Evaluate a survey response against all rules.
        """

        results: list[RuleResult] = []

        for rule in self.rules:

            result = rule.evaluate(response)

            results.append(result)

        return results