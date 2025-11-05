import os
import logging
from datetime import datetime
from output.writers.writer_contract import IWriter

logger = logging.getLogger(__name__)


class JsonWriter(IWriter):

    def execute(self, data: str) -> str:
        try:
            file_name = datetime.now().strftime("report_%Y%m%d%H%M%S.json")
            with open(os.path.join(self.path_result, file_name), "w") as file:
                file.write(data)
            return f"Resultado salvo no path {self.path_result}"
        except Exception as err:
            logger.error(f"Erro ao escrever relatorio no formato json {err}")
            return ""
