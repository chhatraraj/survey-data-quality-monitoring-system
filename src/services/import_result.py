"""
Result object returned after processing a survey import pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ImportResult:
    """
    Represents the outcome of importing and processing
    a survey data file.
    """

    # -------------------------
    # Import Information
    # -------------------------

    source_file: Path

    imported_count: int = 0

    failed_count: int = 0

    skipped_count: int = 0

    # -------------------------
    # Quality Processing
    # -------------------------

    quality_checks: int = 0

    issues_found: int = 0

    alerts_created: int = 0

    # -------------------------
    # Metadata
    # -------------------------

    success: bool = True

    message: str = ""

    processing_time_seconds: float = 0.0