from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from src.database.models.survey_response import SurveyResponse


class CSVMapperInterface(ABC):
    """
    Interface for CSV mappers.
    """

    @abstractmethod
    def map_row(
        self,
        row: dict[str, Any],
        mapping: dict[str, str],
    ) -> SurveyResponse:
        """
        Convert one CSV row into a SurveyResponse.
        """
        raise NotImplementedError