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
