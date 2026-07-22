"""
CSV Mapper.

Converts CSV rows into SurveyResponse ORM objects using
the configured field mapping.
"""

from __future__ import annotations

from datetime import datetime

from src.database.models.survey_response import SurveyResponse
from src.interfaces.csv_mapper import CSVMapperInterface


class CSVMapper(CSVMapperInterface):
    """
    Maps CSV rows to SurveyResponse ORM objects.
    """

    @staticmethod
    def map_row(
        row: dict[str, str],
        mapping: dict[str, str],
    ) -> SurveyResponse:
        """
        Convert a CSV row into a SurveyResponse instance.

        Parameters
        ----------
        row : dict[str, str]
            CSV row represented as a dictionary.

        mapping : dict[str, str]
            Maps logical field names to CSV column names.

        Returns
        -------
        SurveyResponse
            Populated ORM object.
        """

        return SurveyResponse(
            project_id=int(
                CSVMapper._get_required_value(
                    row,
                    mapping,
                    "project_id",
                )
            ),
            form_id=int(
                CSVMapper._get_required_value(
                    row,
                    mapping,
                    "form_id",
                )
            ),
            enumerator_id=int(
                CSVMapper._get_required_value(
                    row,
                    mapping,
                    "enumerator_id",
                )
            ),
            submission_time=datetime.fromisoformat(
                CSVMapper._get_required_value(
                    row,
                    mapping,
                    "submission_time",
                )
            ),
            interview_duration_seconds=CSVMapper._to_int(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "interview_duration_seconds",
                )
            ),
            latitude=CSVMapper._to_float(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "latitude",
                )
            ),
            longitude=CSVMapper._to_float(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "longitude",
                )
            ),
            household_id=CSVMapper._to_none(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "household_id",
                )
            ),
            respondent_age=CSVMapper._to_int(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "respondent_age",
                )
            ),
            district=CSVMapper._to_none(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "district",
                )
            ),
            device_id=CSVMapper._to_none(
                CSVMapper._get_value(
                    row,
                    mapping,
                    "device_id",
                )
            ),
        )

    @staticmethod
    def _get_value(
        row: dict[str, str],
        mapping: dict[str, str],
        field: str,
    ) -> str | None:
        """
        Return the CSV value for an optional field.
        """

        column = mapping.get(field)

        if column is None:
            return None

        return row.get(column)

    @staticmethod
    def _get_required_value(
        row: dict[str, str],
        mapping: dict[str, str],
        field: str,
    ) -> str:
        """
        Return the CSV value for a required field.

        Raises
        ------
        KeyError
            If the mapping or CSV column is missing.
        """

        column = mapping[field]

        if column not in row:
            raise KeyError(
                f"Required CSV column '{column}' not found."
            )

        return row[column]

    @staticmethod
    def _to_int(
        value: str | None,
    ) -> int | None:
        """
        Convert a string to an integer.
        """

        if value in (None, ""):
            return None

        return int(value)

    @staticmethod
    def _to_float(
        value: str | None,
    ) -> float | None:
        """
        Convert a string to a float.
        """

        if value in (None, ""):
            return None

        return float(value)

    @staticmethod
    def _to_none(
        value: str | None,
    ) -> str | None:
        """
        Convert empty strings to None.
        """

        if value is None:
            return None

        value = value.strip()

        if value == "":
            return None

        return value