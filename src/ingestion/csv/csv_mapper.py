"""
CSV Mapper.

Converts CSV rows into SurveyResponse ORM objects.
"""

from __future__ import annotations

from datetime import datetime

from src.database.models.survey_response import SurveyResponse


class CSVMapper:
    """
    Maps CSV rows to SurveyResponse objects.
    """

    @staticmethod
    def map_row(row: dict[str, str]) -> SurveyResponse:
        """
        Convert one CSV row into a SurveyResponse instance.
        """

        return SurveyResponse(
            project_id=int(row["project_id"]),
            form_id=int(row["form_id"]),
            enumerator_id=int(row["enumerator_id"]),
            submission_time=datetime.fromisoformat(
                row["submission_time"]
            ),
            interview_duration_seconds=CSVMapper._to_int(
                row.get("interview_duration_seconds")
            ),
            latitude=CSVMapper._to_float(
                row.get("latitude")
            ),
            longitude=CSVMapper._to_float(
                row.get("longitude")
            ),
            household_id=CSVMapper._to_none(
                row.get("household_id")
            ),
            respondent_age=CSVMapper._to_int(
                row.get("respondent_age")
            ),
            district=CSVMapper._to_none(
                row.get("district")
            ),
            device_id=CSVMapper._to_none(
                row.get("device_id")
            ),
        )

    @staticmethod
    def _to_int(value: str | None) -> int | None:
        """
        Convert string to integer.
        """
        if value in (None, ""):
            return None
        return int(value)

    @staticmethod
    def _to_float(value: str | None) -> float | None:
        """
        Convert string to float.
        """
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def _to_none(value: str | None) -> str | None:
        """
        Convert empty strings to None.
        """
        if value in (None, ""):
            return None
        return value