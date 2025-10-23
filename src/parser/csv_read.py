import csv
import logging
from typing import List, Dict, Any
from utils.validate_struct_csv import validate_columns_csv

logger = logging.getLogger(__name__)


class CsvReaderAdapter:
    def read_data(self, filepath: str) -> List[Dict[str, Any]]:
        try:
            with open(filepath, mode="r", encoding="windows-1252") as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames or not validate_columns_csv(reader.fieldnames):
                    logger.error(
                        f"Erro ao processar arquivo {filepath}: colunas do CSV são inválidas."
                    )
                    return []
                return list(reader)
        except UnicodeDecodeError:
            logger.error(f"Falha ao ler {filepath}.")
            return []
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado em: {filepath}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao ler o arquivo CSV {filepath}: {e}")
            return []
