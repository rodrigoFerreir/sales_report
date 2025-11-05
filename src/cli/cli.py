import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
from utils.cli_message import help_text_cli
from core.parsers.csv_read import CsvReaderAdapter

from output.formatters.json_formater import JsonFormater
from output.formatters.text_formater import TextFormater
from output.writers.writer_contract import IWriter
from output.writers.text_writer import TextWriter
from output.writers.json_writer import JsonWriter
from output.formatters.formater_contract import IFormater

from core.repositories.sale_repository import SalesRepository
from core.services.report_service import SalesReportService


# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the sales report CLI tool.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Ferramenta de linha de comando para processar e analisar dados de vendas a partir de arquivos CSV.",
        epilog=help_text_cli,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "filepath", type=str, help="Caminho para o arquivo CSV de vendas."
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Formato de saída do relatório (text ou json).",
    )
    parser.add_argument(
        "--start-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        help="Data de início para filtrar vendas (formato YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        help="Data de fim para filtrar vendas (formato YYYY-MM-DD).",
    )
    return parser.parse_args()


def _initialize_components() -> (
    Tuple[SalesRepository, SalesReportService, Dict[str, IFormater], Dict[str, IWriter]]
):
    """Initializes and returns instances of core components for the sales report.

    Returns:
        Tuple[SalesRepository, SalesReportService, Dict[str, IFormater], Dict[str, IWriter]]:
            A tuple containing the sales repository, report service, formatters, and writers.
    """
    csv_data_reader = CsvReaderAdapter()
    repository = SalesRepository(csv_data_reader)
    service = SalesReportService()

    formatters: Dict[str, IFormater] = {
        "json": JsonFormater(),
        "text": TextFormater(),
    }

    writers: Dict[str, IWriter] = {
        "json": JsonWriter(),
        "text": TextWriter(),
    }
    return repository, service, formatters, writers


def _process_and_report(
    args: argparse.Namespace,
    repository: SalesRepository,
    service: SalesReportService,
    formatters: Dict[str, IFormater],
    writers: Dict[str, IWriter],
):
    """Processes sales data, generates a report, and outputs it based on the provided arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        repository (SalesRepository): The sales data repository instance.
        service (SalesReportService): The sales report service instance.
        formatters (Dict[str, IFormater]): Dictionary of available report formatters.
        writers (Dict[str, IWriter]): Dictionary of available report writers.
    """
    absolute_filepath = Path(args.filepath).resolve()
    if not absolute_filepath.is_file():
        logging.error(f"O arquivo não foi encontrado em: {absolute_filepath}")
        return

    sales_generator = repository.load_sales(str(absolute_filepath))
    sales_data = list(sales_generator)

    if not sales_data:
        logging.warning("Nenhum dado de venda válido foi carregado. Verifique o arquivo.")
        return

    report = service.generate_report(
        sales=sales_data,
        start_date=args.start_date,
        end_date=args.end_date,
    )

    formatter = formatters[args.format]
    writer = writers[args.format]

    data = formatter.execute(report.to_dict())
    result = writer.execute(data)

    print("RESULTADO DO RELATÓRIO")
    print(data)
    print(result)


def main():
    args = _parse_arguments()
    repository, service, formatters, writers = _initialize_components()

    try:
        _process_and_report(args, repository, service, formatters, writers)
    except FileNotFoundError:
        logging.error(f"O arquivo não foi encontrado em: {args.filepath}")
    except ValueError as e:
        logging.error(f"Erro de formato de data ou valor inválido: {e}")
    except TypeError as e:
        logging.error(f"Erro de tipo ao processar dados: {e}")
    except KeyError as e:
        logging.error(f"Coluna CSV ausente ou inválida: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
