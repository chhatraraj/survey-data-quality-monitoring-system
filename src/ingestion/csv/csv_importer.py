"""
CSV Import Service.

Imports survey responses from CSV into PostgreSQL.
"""

from pathlib import Path

from sqlalchemy.orm import Session

from src.config.field_mapping import load_field_mapping
from src.database.repositories.response_repository import (
    SurveyResponseRepository,
)
from src.ingestion.csv.csv_mapper import CSVMapper
from src.ingestion.csv.csv_reader import CSVReader


class CSVImporter:
    """
    Imports survey responses from a CSV file.
    """

    def __init__(
        self,
        session: Session,
        repository: SurveyResponseRepository,
    ) -> None:
        self.session = session
        self.repository = repository

    def import_file(self, csv_file: str | Path) -> int:
        """
        Import a CSV file into the database.

        Returns
        -------
        int
            Number of imported survey responses.
        """

        mapping = load_field_mapping()

        reader = CSVReader(csv_file)

        imported = 0

        for row in reader.read():

            response = CSVMapper.map_row(
                row=row,
                mapping=mapping,
            )

            self.repository.create(
                response,
                commit=False,
            )

            imported += 1

        self.session.commit()

        return imported