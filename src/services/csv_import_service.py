"""
CSV Import Service.

Coordinates the CSV import workflow by orchestrating
the reader, mapper, and repository.
"""

from __future__ import annotations

import logging

from src.database.repositories.response_repository import (
    SurveyResponseRepository,
)
from src.interfaces.csv_reader import CSVReaderInterface
from src.interfaces.csv_mapper import CSVMapperInterface

logger = logging.getLogger(__name__)


class CSVImportService:
    """
    Service responsible for importing survey responses
    from CSV files into the database.
    """

    def __init__(
        self,
        reader: CSVReaderInterface,
        mapper: CSVMapperInterface,
        repository: SurveyResponseRepository,
    ) -> None:
        self.reader = reader
        self.mapper = mapper
        self.repository = repository