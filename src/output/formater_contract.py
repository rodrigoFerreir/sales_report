from abc import ABC
from typing import Dict, Any


class IFormater(ABC):

    @staticmethod
    def execute(report_data: Dict[str, Any]) -> str: ...
