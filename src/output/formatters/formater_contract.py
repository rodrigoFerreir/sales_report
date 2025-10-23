from abc import ABC
from typing import Dict, Any


class IFormater(ABC):

    def __init__(self) -> None:
        super().__init__()

    def execute(self, report_data: Dict[str, Any]) -> str: ...
