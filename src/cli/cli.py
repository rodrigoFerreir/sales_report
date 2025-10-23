import argparse
import logging
from pathlib import Path
from typing import Dict, Protocol
from datetime import datetime
from core.repository import SalesRepository
from core.services import SalesReportService
from parser.csv_read import CsvReaderAdapter
from output.json_formater import JsonFormater
from output.text_formater import TextFormater

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    parser = argparse.ArgumentParser(
        description="Ferramenta de linha de comando para processar e analisar dados de vendas a partir de arquivos CSV.",
        epilog="""
Exemplos de uso:
  1. Gerar um relatório de vendas em formato de texto:
     python -m src.cli.cli data/vendas.csv

  2. Gerar um relatório de vendas em formato JSON:
     python -m src.cli.cli data/vendas.csv --format json

  3. Filtrar vendas por um período específico:
     python -m src.cli.cli data/vendas.csv --start-date 2023-01-01 --end-date 2023-12-31

Argumentos:
  filepath      Caminho para o arquivo CSV de vendas.

Opções:
  --format      Formato de saída do relatório (text ou json). Padrão: text.
  --start-date  Data de início para filtrar vendas (formato YYYY-MM-DD).
  --end-date    Data de fim para filtrar vendas (formato YYYY-MM-DD).
  --help        Mostra esta mensagem de ajuda e sai.
""",
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

    args = parser.parse_args()

    absolute_filepath = Path(args.filepath).resolve()
    if not absolute_filepath.is_file():
        logging.error(f"O arquivo não foi encontrado em: {absolute_filepath}")
        return

    repository = SalesRepository(CsvReaderAdapter())
    service = SalesReportService()

    formatters = {
        "json": JsonFormater,
        "text": TextFormater,
    }

    try:
        sales_data = repository.load_sales(str(absolute_filepath))
        if not sales_data:
            logging.warning("Nenhum dado de venda foi carregado. Verifique o arquivo.")
            return

        report = service.generate_report(
            sales=sales_data,
            start_date=args.start_date,
            end_date=args.end_date,
        )

        formatter = formatters[args.format]
        data = formatter.execute(report.to_dict())
        print("RESULTADO DO RELATÓRIO")
        print(data)

    except FileNotFoundError:
        logging.error(f"O arquivo não foi encontrado em: {absolute_filepath}")
    except (ValueError, TypeError) as e:
        logging.error(f"Erro ao processar os dados de vendas: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
