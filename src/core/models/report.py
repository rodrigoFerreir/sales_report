from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


@dataclass
class Report:
    total_per_product: Dict[str, Decimal]
    value_total_sales: Decimal
    product_more_saled: tuple | None
    total_sales_processed: int

    def __str__(self):
        return f"Report total sales processed: {self.total_sales_processed}"

    def to_dict(self):
        return {
            "total_por_produto": self.total_per_product,
            "valor_total_vendas": self.value_total_sales,
            "produto_mais_vendido": self.product_more_saled,
            "total_vendas_processadas": self.total_sales_processed,
        }
