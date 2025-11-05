import logging
from core.models.sale import Sale
from typing import Any, Dict, Generator
from dateutil.parser import parse as date_parse
from decimal import Decimal, InvalidOperation, ConversionSyntax
from core.parsers.parser_contract import DataReaderContract

logger = logging.getLogger(__name__)


class SalesRepository:
    """Manages the loading of sales data from a- data source using a DataReader."""

    def __init__(self, data_reader: DataReaderContract):
        """Initializes the SalesRepository with a data reader.

        Args:
            data_reader (DataReader): An object conforming to the DataReader protocol.
        """
        self.data_reader = data_reader

    def _validate_values(self, row: Dict[str, Any]):
        quantity = str(row["quantidade"])
        price = str(row["preco_unitario"])

        if not quantity or not quantity.isdigit():
            raise ValueError(
                f"O campo 'quantidade' deve ser um numero inteiro foi recebido ({quantity})"
            )
        if not price or not price.split(".")[0].isnumeric():
            raise ValueError(
                f"O campo 'preco_unitario' deve ser um numero decimal foi recebido ({price})"
            )

    def load_sales(self, filepath: str) -> Generator[Sale, None, None]:
        """Loads sales data from the specified file and yields Sale objects.

        Args:
            filepath (str): The path to the sales data file.

        Yields:
            Generator[Sale, None, None]: A generator of Sale objects.
        """
        sales_data = self.data_reader.read_data(filepath)

        for i, row in enumerate(sales_data):
            try:

                sale_date = date_parse(row["data"]).date() if row.get("data") else None
                self._validate_values(row)

                sale = Sale(
                    product=row["produto"],
                    quantity=int(row["quantidade"]),
                    price=Decimal(row["preco_unitario"]),
                    data=sale_date,
                )
                yield sale
            except ConversionSyntax as e:
                logger.warning(
                    f"Ignorando linha {i + 2} - {row} para converter valor para decimal"
                )
                continue
            except (ValueError, TypeError, KeyError, InvalidOperation) as e:
                logger.warning(
                    f"Ignorando linha {i + 2} com dados inválidos: {row}. Erro: {e}"
                )
                continue
