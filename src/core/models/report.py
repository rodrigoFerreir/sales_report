from dataclasses import dataclass


@dataclass
class Report:
    total_per_product: dict
    value_total_sales: float
    product_more_saled: tuple | None
    total_sales_processed: int

    def to_dict(self):
        return {
            "total_por_produto": self.total_per_product,
            "valor_total_vendas": self.value_total_sales,
            "produto_mais_vendido": self.product_more_saled,
            "total_vendas_processadas": self.total_sales_processed,
        }
