# ETL, CSV imports, KoboToolbox API, and even future FastAPI endpoints will 
# all call the same QualityService instead of talking directly to the RuleEngine.

"""
Quality Service.

Provides a high-level interface for validating
survey responses using the Rule Engine.
"""

from src.database.models.survey_response import SurveyResponse
from src.quality.engine import RuleEngine
from src.quality.rule_result import RuleResult


class QualityService:
    """
    Service responsible for executing quality validation
    workflows for survey responses.
    """

    def __init__(
        self,
        engine: RuleEngine,
    ) -> None:
        """
        Initialize the service.

        Parameters
        ----------
        engine:
            Configured RuleEngine instance.
        """

        self.engine = engine

    def validate(
        self,
        response: SurveyResponse,
    ) -> list[RuleResult]:
        """
        Validate a survey response.

        Parameters
        ----------
        response:
            Survey response to validate.

        Returns
        -------
        list[RuleResult]
            Results returned by the Rule Engine.
        """

        return self.engine.process(response)