import pytest
from pathlib import Path
import os


@pytest.fixture
def sales_csv_file(tmp_path):
    content = (
        "produto,preco_unitario,quantidade\n"
        "ProdutoA,10.50,2\n"
        "ProdutoB,20.00,1\n"
        "ProdutoA,10.50,3\n"
        "ProdutoC,5.00,10\n"
    )
    file_path = tmp_path / "test_sales.csv"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def sales_csv_file_with_date(tmp_path):
    content = (
        "produto,preco_unitario,quantidade,data\n"
        "ProdutoA,10.50,2,2025-10-21\n"
        "ProdutoB,20.00,1,2025-10-22\n"
        "ProdutoA,10.50,3,2025-10-23\n"
        "ProdutoC,5.00,10,2025-10-24\n"
        "ProdutoB,20.00,3,2025-10-25\n"
        "ProdutoA,10.50,5,2025-10-26\n"
    )
    file_path = tmp_path / "test_sales_with_date.csv"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def malformed_test_sales(tmp_path):
    malformed_content = (
        "produto,preco_unitario,quantidade,data\n"
        "ProdutoX,abc,1,2025-01-01\n"  # invalid price
        "ProdutoY,10.00,def,2025-01-02\n"  # invalid quantity
        "ProdutoZ,20.00,2,invalid-date\n"  # invalid data
    )
    file_path = tmp_path / "malformed_test_sales.csv"
    file_path.write_text(malformed_content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def invalid_columns_test_sales(tmp_path):
    invalid_columns_content = (
        "nome_produto,preco,qtd,data_venda\n" "ProdutoA,10.0,5,2025-01-01\n"
    )
    file_path = tmp_path / "invalid_columns_test_sales.csv"
    file_path.write_text(invalid_columns_content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def sales_empty_file(tmp_path):
    file_path = tmp_path / "empty_test_sales.csv"
    file_path.write_text("produto,preco_unitario,quantidade,data\n", encoding="utf-8")
    return str(file_path)
