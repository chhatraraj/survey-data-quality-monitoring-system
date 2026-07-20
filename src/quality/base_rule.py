"""
Base class for all survey quality validation rules.
"""

from abc import ABC
from abc import abstractmethod

from src.database.models.survey_response import SurveyResponse
from src.quality.rule_result import RuleResult


class BaseRule(ABC):
    """
    Abstract base class for all quality rules.
    """

    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        self.name = name
        self.description = description

    @property
    def rule_name(self) -> str:
        """
        Human-readable name of the rule.
        """
        return self.name

    def process(
        self,
        response: SurveyResponse,
    ) -> RuleResult:
        """
        Public entry point used by the RuleEngine.
        """

        return self.evaluate(response)

    @abstractmethod
    def evaluate(
        self,
        response: SurveyResponse,
    ) -> RuleResult:
        """
        Execute the validation rule.
        """
        ...