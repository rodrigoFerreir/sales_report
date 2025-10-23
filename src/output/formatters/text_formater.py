import logging
from typing import Dict, Any
from output.formatters.formater_contract import IFormater

logger = logging.getLogger(__name__)


class TextFormater(IFormater):
    def execute(self, report_data: Dict[str, Any]) -> str:
        try:
            output = []
            output.append("+----------------------------------------+")
            output.append("|         Relatório de Vendas            |")
            output.append("+----------------------------------------+")
            output.append("| Total de Vendas por Produto            |")
            output.append("+---------------------+------------------+")
            output.append("| Produto             | Valor            |")
            output.append("+---------------------+------------------+")

            if report_data["total_por_produto"]:
                for product, total in report_data["total_por_produto"].items():
                    output.append(f"| {product:<20}| R$ {total:<15.2f} |")
            else:
                output.append("| Nenhuma venda encontrada.              |")

            output.append("+---------------------+------------------+")
            output.append("| Resumo                                 |")
            output.append("+----------------------------------------+")

            total_sales_str = f"Valor Total de Vendas: R$ {report_data.get('valor_total_vendas', 0.0):.2f}"
            output.append(f"| {total_sales_str:<38} |")

            if report_data["produto_mais_vendido"]:
                product, quantity = report_data["produto_mais_vendido"]
                best_seller_str = (
                    f"Produto Mais Vendido: {product} ({quantity} unidades)"
                )
                output.append(f"| {best_seller_str:<38} |")
            else:
                output.append("| Produto Mais Vendido: Nenhum           |")

            processed_sales_str = f"Total de Vendas Processadas: {report_data.get('total_vendas_processadas')}"
            output.append(f"| {processed_sales_str:<38} |")
            output.append("+----------------------------------------+")

            return "\n".join(output)
        except Exception as err:
            logger.error(f"Erro ao gerar relatorio no fomato txt {err}")
            return ""
