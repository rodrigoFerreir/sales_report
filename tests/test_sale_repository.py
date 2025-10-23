import pytest
from datetime import date
from core.models.sale import Sale
from core.repository import SalesRepository
from src.parser.csv_read import CsvReaderAdapter


@pytest.fixture
def repository_sales():
    return SalesRepository(CsvReaderAdapter())


def test_load_sales_success(repository_sales, sales_csv_file):
    sales = repository_sales.load_sales(sales_csv_file)
    assert len(sales) == 4
    assert isinstance(sales[0], Sale)
    assert sales[0].product == "ProdutoA"
    assert sales[0].price == 10.50
    assert sales[0].quantity == 2

    assert sales[1].product == "ProdutoB"
    assert sales[1].price == 20.00
    assert sales[1].quantity == 1


def test_load_sales_file_not_found(repository_sales):
    sales = repository_sales.load_sales("non_existent_file.csv")
    assert sales == []


def test_load_sales_with_data(repository_sales, sales_csv_file_with_date):
    sales = repository_sales.load_sales(sales_csv_file_with_date)
    assert len(sales) == 6
    assert isinstance(sales[0], Sale)
    assert isinstance(sales[0].data, date)
    assert isinstance(sales[3].data, date)


def test_load_sales_malformed_data(repository_sales, malformed_test_sales):
    sales = repository_sales.load_sales(malformed_test_sales)
    assert len(sales) == 0


def test_load_sales_invalid_columns(repository_sales, invalid_columns_test_sales):
    sales = repository_sales.load_sales(invalid_columns_test_sales)
    assert len(sales) == 0


def test_load_sales_empty_file(repository_sales, sales_empty_file):
    sales = repository_sales.load_sales(sales_empty_file)
    assert len(sales) == 0
