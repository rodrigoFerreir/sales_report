import logging
from datetime import date
from collections import Counter
from core.models.sale import Sale
from core.models.report import Report
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class SalesReportService:

    def generate_report(
        self,
        sales: List[Sale],
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        filtered_sales = self._filter_sales_by_date(sales, start_date, end_date)

        total_per_produt = self._calculate_total_per_product(filtered_sales)
        value_total_sales = sum(total_per_produt.values())
        product_more_saled = self._find_best_selling_product(filtered_sales)
        return Report(
            total_per_produt,
            value_total_sales,
            product_more_saled,
            len(filtered_sales),
        )

    def _filter_sales_by_date(
        self,
        sales: List[Sale],
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Sale]:
        data = []
        try:
            if not start_date and not end_date:
                return sales

            for sale in sales:
                if not sale.data:
                    continue
                if start_date <= sale.data <= end_date:
                    data.append(sale)

            return data
        except (TypeError, ValueError) as err:
            logger.error(f"Error ao filtrar resultados de vendas {err} ")
            return data

    def _calculate_total_per_product(self, sales: List[Sale]) -> Dict[str, float]:
        try:
            totals: Dict[str, float] = {}
            for sale in sales:
                totals[sale.product] = totals.get(sale.product, 0.0) + (
                    sale.price * sale.quantity
                )
            return totals
        except (TypeError, KeyError) as err:
            logger.error(f"Erro ao calcular total de vendas por produto {err}")
            return {}

    def _find_best_selling_product(self, sales: List[Sale]):
        try:
            if not sales:
                return None

            product_quantities = Counter()
            for sale in sales:
                product_quantities[sale.product] += sale.quantity

            most_common = product_quantities.most_common(1)
            if most_common:
                return most_common[0]

            return None
        except (TypeError, KeyError) as err:
            logger.error(f"Error ao buscar o produto mais vendido {err}")
            return None
