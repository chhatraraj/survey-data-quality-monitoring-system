"""
Represents the result of a CSV import.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ImportResult:
    total_rows: int
    imported_rows: int
    failed_rows: int