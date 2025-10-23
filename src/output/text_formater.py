from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TextFormater:

    @staticmethod
    def execute(report_data: Dict[str, Any]) -> str:
        try:
            output = []
            output.append("\n--- Relatório de Vendas ---")
            output.append("\nTotal de Vendas por Produto:")

            if report_data["total_por_produto"]:
                for product, total in report_data["total_por_produto"].items():
                    output.append(f"  - {product}: R$ {total:.2f}")
            else:
                output.append("  Nenhuma venda por produto encontrada.")

            output.append(
                f"\nValor Total de Todas as Vendas: R$ {report_data.get('valor_total_vendas', 0.0):.2f}"
            )

            output.append("\nProduto Mais Vendido:")
            if report_data["produto_mais_vendido"]:
                product, quantity = report_data["produto_mais_vendido"]
                output.append(f"  - {product} (Total de {quantity} unidades vendidas)")
            else:
                output.append("  Nenhum produto mais vendido encontrado.")

            output.append(
                f"\nTotal de Vendas Processadas: {report_data.get('total_vendas_processadas')}"
            )
            output.append("-" * 20)

            return "\n".join(output)
        except Exception as err:
            logger.error(f"Erro ao gerar relatorio no fomato txt {err}")
