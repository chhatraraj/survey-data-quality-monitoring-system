"""
CSV Reader.

Reads survey data from CSV files.
"""

from __future__ import annotations

import csv
from pathlib import Path


class CSVReader:
    """
    Reads survey responses from a CSV file.
    """

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def read(self) -> list[dict[str, str]]:
        """
        Read the CSV file.

        Returns
        -------
        list[dict[str, str]]
            Each row represented as a dictionary using
            the CSV header as keys.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        with self.file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            return list(reader)