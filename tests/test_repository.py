import pytest
from core.models.sale import Sale
from core.repository import SalesRepository
from src.parser.csv_read import CsvReaderAdapter


@pytest.fixture
def repo():
    return SalesRepository(CsvReaderAdapter())


def test_load_sales_success(repo, sales_csv_file):
    sales = repo.load_sales(sales_csv_file)
    assert len(sales) == 4
    assert isinstance(sales[0], Sale)
    assert sales[0].product == "ProdutoA"
    assert sales[0].price == 10.50
    assert sales[0].quantity == 2

    assert sales[1].product == "ProdutoB"
    assert sales[1].price == 20.00
    assert sales[1].quantity == 1


def test_load_sales_file_not_found(repo):
    sales = repo.load_sales("non_existent_file.csv")
    assert sales == []


def test_load_sales_with_data(repo, tmp_path):
    with_data_csv_path = tmp_path / "test_sales_with_data.csv"
    with_data_csv_content = (
        "produto,preco_unitario,quantidade,data\n"
        "ProdutoX,30.00,1,2025-01-01\n"
        "ProdutoY,10.00,8,2025-01-02\n"
        "ProdutoZ,20.00,2,2025-01-02\n"
    )
    with_data_csv_path.write_text(with_data_csv_content, encoding="utf-8")

    sales = repo.load_sales(str(with_data_csv_path))
    assert len(sales) == 3


def test_load_sales_malformed_data(repo, tmp_path):
    malformed_csv_path = tmp_path / "malformed_test_sales.csv"
    malformed_content = (
        "produto,preco_unitario,quantidade,data\n"
        "ProdutoX,abc,1,2025-01-01\n"  # invalid price
        "ProdutoY,10.00,def,2025-01-02\n"  # invalid quantity
        "ProdutoZ,20.00,2,invalid-date\n"  # invalid data
    )
    malformed_csv_path.write_text(malformed_content, encoding="utf-8")

    sales = repo.load_sales(str(malformed_csv_path))
    assert len(sales) == 0


def test_load_sales_invalid_columns(repo, tmp_path):
    invalid_columns_csv_path = tmp_path / "invalid_columns_test_sales.csv"
    invalid_columns_content = (
        "nome_produto,preco,qtd,data_venda\n" "ProdutoA,10.0,5,2025-01-01\n"
    )
    invalid_columns_csv_path.write_text(invalid_columns_content, encoding="utf-8")

    sales = repo.load_sales(str(invalid_columns_csv_path))
    assert len(sales) == 0


def test_load_sales_empty_file(repo, tmp_path):
    empty_csv_path = tmp_path / "empty_test_sales.csv"
    empty_csv_path.write_text(
        "produto,preco_unitario,quantidade,data\n", encoding="utf-8"
    )
    sales = repo.load_sales(str(empty_csv_path))
    assert len(sales) == 0
