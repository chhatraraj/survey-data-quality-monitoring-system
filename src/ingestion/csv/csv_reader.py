"""
CSV Reader.

Reads CSV files and yields each row as a dictionary.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator


class CSVReader:
    """
    Reads CSV files using DictReader.

    Every row is returned as:

    {
        "SubmissionDate": "...",
        "EnumeratorID": "...",
        ...
    }
    """

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def read(self) -> Iterator[dict[str, str]]:
        """
        Read CSV file row by row.

        Yields
        ------
        dict
            One CSV row.
        """

        with self.file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:
                yield row