import os
from abc import ABC
from typing import Dict, Any


class IWriter(ABC):

    def __init__(self) -> None:
        self.path_result = os.path.join("data", "result")
        os.makedirs(self.path_result, exist_ok=True)
        super().__init__()

    def execute(self, data: str) -> str: ...
