"""
CSV Import Service.

Coordinates the CSV import workflow by orchestrating
the reader, mapper, and repository.
"""

from __future__ import annotations

from src.database.repositories.response_repository import (
    SurveyResponseRepository,
)
from src.ingestion.csv_mapper import CSVMapper
from src.ingestion.csv_reader import CSVReader


class CSVImportService:
    """
    Service responsible for importing survey responses
    from CSV files into the database.
    """

    def __init__(
        self,
        reader: CSVReader,
        mapper: CSVMapper,
        repository: SurveyResponseRepository,
    ) -> None:
        self.reader = reader
        self.mapper = mapper
        self.repository = repository