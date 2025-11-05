import logging
from datetime import date
from collections import Counter
from decimal import Decimal
from core.models.sale import Sale
from core.models.report import Report
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class SalesReportService:
    """Service class for generating sales reports based on a list of sales.
    """

    def generate_report(
        self,
        sales: List[Sale],
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Report:
        """Generates a sales report based on the provided sales data and date filters.

        Args:
            sales (List[Sale]): A list of Sale objects.
            start_date (Optional[date]): The start date for filtering sales (inclusive).
            end_date (Optional[date]): The end date for filtering sales (inclusive).

        Returns:
            Report: An object containing the generated sales report.
        """
        filtered_sales = self._filter_sales_by_date(sales, start_date, end_date)

        total_per_produt = self._calculate_total_per_product(filtered_sales)
        value_total_sales = sum(total_per_produt.values())
        product_more_saled = self._find_best_selling_products(filtered_sales)
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
        """Filters a list of sales by a given date range.

        Args:
            sales (List[Sale]): The list of sales to filter.
            start_date (Optional[date]): The start date for filtering (inclusive).
            end_date (Optional[date]): The end date for filtering (inclusive).

        Returns:
            List[Sale]: A new list containing only the sales within the specified date range.

        Raises:
            ValueError: If there's an issue with date comparison or filtering.
        """
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
            raise err

    def _calculate_total_per_product(self, sales: List[Sale]) -> Dict[str, Decimal]:
        """Calculates the total revenue for each product in a list of sales.

        Args:
            sales (List[Sale]): The list of sales.

        Returns:
            Dict[str, float]: A dictionary where keys are product names and values are their total revenues.

        Raises:
            ValueError: If there's an issue with calculating totals (e.g., invalid price or quantity).
        """
        try:
            totals: Dict[str, Decimal] = {}
            for sale in sales:
                totals[sale.product] = totals.get(sale.product, Decimal("0.0")) + (
                    sale.price * sale.quantity
                )
            return totals
        except (TypeError, KeyError) as err:
            logger.error(f"Erro ao calcular total de vendas por produto {err}")
            raise err
    def _find_best_selling_products(self, sales: List[Sale]) -> List[Tuple[str, int]]:
        """Identifies the best-selling products based on quantity sold.

        Args:
            sales (List[Sale]): The list of sales.

        Returns:
            List[Tuple[str, int]]: A list of tuples, where each tuple contains the product name and the total quantity sold for best-selling products.

        Raises:
            ValueError: If there's an issue with processing product quantities.
        """
        try:
            if not sales:
                return []

            product_quantities = Counter()
            for sale in sales:
                product_quantities[sale.product] += sale.quantity
            if not product_quantities:
                return []

            top_sellers = []
            max_quantity = product_quantities.most_common(1)[0][1]
            for product, quantity in product_quantities.items():
                if quantity == max_quantity:
                    top_sellers.append((product, quantity))

            return top_sellers

        except (TypeError, KeyError, IndexError) as err:
            logger.error(f"Erro ao buscar os produtos mais vendidos: {err}")
            raise err
