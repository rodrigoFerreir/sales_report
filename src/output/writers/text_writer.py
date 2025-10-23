import os
import logging
from datetime import datetime
from output.writers.writer_contract import IWriter

logger = logging.getLogger(__name__)


class TextWriter(IWriter):

    def execute(self, data: str) -> str:
        try:
            file_name = datetime.now().strftime("report_%Y%m%d%H%M%S.txt")
            with open(os.path.join(self.path_result, file_name), "w") as file:
                file.writelines(data)
            return f"Resultado salvo no path {self.path_result}"
        except Exception as err:
            logger.error(f"Erro ao criar relatorio no formato text {err}")
            return ""
