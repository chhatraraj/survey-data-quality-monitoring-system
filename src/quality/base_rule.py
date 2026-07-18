"""
Base class for all survey quality validation rules.
"""

from abc import ABC, abstractmethod

from src.database.models.survey_response import SurveyResponse
from src.quality.rule_result import RuleResult


class BaseRule(ABC):
    """
    Abstract base class for all quality rules.

    Every rule must inherit from this class and implement
    the evaluate() method.
    """

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @property
    @abstractmethod
    def rule_name(self) -> str:
        """
        Human-readable name of the rule.
        """
        ...

    @abstractmethod
    def evaluate(self, response: SurveyResponse) -> RuleResult:
        """
        Evaluate a survey response.

        Parameters
        ----------
        response : SurveyResponse
            Survey response to validate.

        Returns
        -------
        RuleResult
            Result of the validation.
        """
        ...