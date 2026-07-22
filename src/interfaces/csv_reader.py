from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class CSVReaderInterface(ABC):
    """
    Interface for CSV readers.
    """

    @abstractmethod
    def read(self, file_path: str) -> list[dict[str, Any]]:
        """
        Read a CSV file.
        """
        raise NotImplementedError