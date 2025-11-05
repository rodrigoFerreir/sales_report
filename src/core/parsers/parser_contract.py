from typing import Any, Dict, Generator
from abc import ABC, abstractmethod


class DataReaderContract(ABC):

    @abstractmethod
    def read_data(self, filepath: str) -> Generator[Dict[str, Any], None, None]: ...
