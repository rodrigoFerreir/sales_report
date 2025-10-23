import logging
from typing import List, Protocol
from datetime import datetime
from core.models.sale import Sale

logger = logging.getLogger(__name__)


class DataReader(Protocol):
    def read_data(self, filepath: str): ...


class SalesRepository:
    def __init__(self, data_reader: DataReader):
        self.data_reader = data_reader

    def load_sales(self, filepath: str):
        sales_data = self.data_reader.read_data(filepath)
        sales: List[Sale] = []

        for row in sales_data:
            try:
                sale = Sale(
                    product=row["produto"],
                    quantity=int(row["quantidade"]),
                    price=float(row["preco_unitario"]),
                    data=(
                        datetime.strptime(row["data"], "%Y-%m-%d").date()
                        if "data" in row and row["data"]
                        else None
                    ),
                )
                sales.append(sale)
            except (ValueError, KeyError) as e:
                logger.warning(f"Ignorando linha com dados inválidos: {row}. Erro: {e}")
                continue

        return sales
