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
from src.interfaces.csv_mapper import CSVMapperInterface
from src.interfaces.csv_reader import CSVReaderInterface
from src.services.import_result import ImportResult

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

    def import_file(
        self,
        csv_path: str,
        mapping: dict[str, str],
    ) -> ImportResult:
        """
        Import survey responses from a CSV file.

        - Reads raw CSV rows using reader (Step 3)
        - Maps rows into ORM instances via mapper using field configuration (Step 4)
        - Persists mapped responses through repository (Step 5)
        - Handles per-row mapping/validation errors (Step 6)
        - Commits successful transactions or rolls back on critical errors (Step 7)
        """
        # Step 3: Read raw rows from file
        rows = self.reader.read(csv_path)

        total_rows = len(rows)
        imported = 0
        failed = 0

        # Steps 4, 5, 6: Row processing with mapping, repository save, and error isolation
        for index, row in enumerate(rows, start=1):
            try:
                # Step 4: Map row with configured column mapping
                response = self.mapper.map_row(
                    row=row,
                    mapping=mapping,
                )

                # Step 5: Stage response model in repository
                self.repository.add(response)

                imported += 1

            except Exception as exc:
                # Step 6: Isolate row failures and log trace
                failed += 1
                logger.exception(
                    "Failed to import row %s: %s",
                    index,
                    exc,
                )

        # Step 7: Transaction management with commit and rollback handling
        try:
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise

        return ImportResult(
            total_rows=total_rows,
            imported_rows=imported,
            failed_rows=failed,
        )