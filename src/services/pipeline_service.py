"""
Pipeline Service.

Coordinates the complete survey processing workflow.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.services.csv_import_service import CSVImportService
from src.services.quality_service import QualityService
from src.services.import_result import ImportResult

logger = logging.getLogger(__name__)


class PipelineService:
   

    def __init__(
        self,
        csv_import_service: CSVImportService,
        quality_service: QualityService,
    ) -> None:
        
        self.csv_import_service = csv_import_service
        self.quality_service = quality_service

    def process_file(
        self,
        csv_path: Path,
        mapping_path: Path,
    ) -> ImportResult:
      
        logger.info(
            "Starting pipeline for file=%s using mapping=%s",
            csv_path,
            mapping_path,
        )


        # STEP 1: Import
        # CSVImportService internally does the CSV reading, the column
        # mapping, and the save-to-PostgreSQL. PipelineService doesn't
  
        import_result: ImportResult = self.csv_import_service.import_file(
            csv_path=csv_path,
            mapping_path=mapping_path,
        )

        logger.info(
            "Import finished: %d rows imported, %d rows failed",
            import_result.rows_imported,
            import_result.rows_failed,
        )

        
        # STEP 2: Quality Validation
        # Only run quality checks on what was actually imported. If
        
        if import_result.rows_imported > 0:
            quality_result = self.quality_service.run_quality_checks(
                survey_response_ids=import_result.imported_ids,
            )
            logger.info(
                "Quality checks finished: %d alerts raised",
                len(quality_result.alerts),
            )
            import_result.quality_result = quality_result
        else:
            logger.warning(
                "Skipping quality checks — no rows were imported from %s",
                csv_path,
            )

        
        # STEP 3: Return the summary
      
        logger.info("Pipeline complete for file=%s", csv_path)
        return import_result