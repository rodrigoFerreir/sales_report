import csv
import logging
from utils.validate_struct_csv import validate_columns_csv
from core.parsers.parser_contract import DataReaderContract

logger = logging.getLogger(__name__)


class CsvReaderAdapter(DataReaderContract):

    def __read(self, filepath: str, encoding: str = "utf-8"):
        try:
            with open(filepath, mode="r", encoding=encoding, errors="strict") as file:
                data = csv.DictReader(file)
                columns = list(data.fieldnames)  # type: ignore
                if not columns or not validate_columns_csv(columns):
                    logger.error(
                        f"Erro ao processar arquivo {filepath}: colunas do CSV são inválidas ou ausentes."
                    )
                    return []
                yield from data
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado em: {filepath}")
            raise
        except UnicodeDecodeError:
            logger.error(
                f"Erro de decodificação no arquivo {filepath} com encoding {encoding}. Tentando 'windows-1252'..."
            )
            raise
        except csv.Error as e:
            logger.error(f"Erro ao ler CSV do arquivo {filepath}: {e}")
            raise
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado ao ler o arquivo {filepath}: {e}")
            raise

    def read_data(self, filepath: str):
        try:
            yield from self.__read(filepath)
        except UnicodeDecodeError:
            try:
                yield from self.__read(filepath, "windows-1252")
            except Exception:
                return
        except Exception:
            return
