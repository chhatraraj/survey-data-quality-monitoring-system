def process_file(
    self,
    csv_path: Path,
    mapping_path: Path,
) -> ImportResult:
    """
    Process one CSV file through the survey pipeline.
    """

    logger.info("=" * 60)
    logger.info("Starting survey processing pipeline.")
    logger.info("CSV File: %s", csv_path)
    logger.info("Mapping File: %s", mapping_path)

    import_result = self.csv_import_service.import_file(
        csv_path=csv_path,
        mapping_path=mapping_path,
    )

    logger.info(
        "CSV import completed. Imported %s responses.",
        import_result.imported_count,
    )

    return import_result