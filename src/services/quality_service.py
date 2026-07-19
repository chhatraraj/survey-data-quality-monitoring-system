from src.database.models.survey_response import SurveyResponse
from src.quality.engine import RuleEngine


class QualityService:
    """
    Service responsible for validating survey responses.
    """

    def __init__(self, engine: RuleEngine):
        self.engine = engine

    def validate(self, response: SurveyResponse):
        return self.engine.process(response)