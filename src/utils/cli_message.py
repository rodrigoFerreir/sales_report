help_text_cli = """
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
"""
