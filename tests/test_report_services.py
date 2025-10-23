import pytest
from typing import List
from datetime import date

from core.models.sale import Sale
from core.models.report import Report
from core.services import SalesReportService


@pytest.fixture
def sales_data() -> List[Sale]:
    return [
        Sale("Laptop", 3500.50, 2, date(2025, 10, 20)),
        Sale("Mouse", 150.00, 5, date(2025, 10, 21)),
        Sale("Teclado", 300.25, 3, date(2025, 10, 21)),
        Sale("Monitor", 800.00, 1, date(2025, 10, 22)),
        Sale("Laptop", 3400.00, 1, date(2025, 10, 22)),
        Sale("Fone de ouvido", 200.00, 4, date(2025, 10, 23)),
        Sale("Mouse", 160.00, 2, date(2025, 10, 23)),
    ]


@pytest.fixture
def service() -> SalesReportService:
    return SalesReportService()


def test_generate_report_no_filter(service, sales_data):
    """testa a geração de um relatorio sem filtro por data"""
    report = service.generate_report(sales_data)
    report_dict = report.to_dict()

    assert "total_por_produto" in report_dict
    assert "valor_total_vendas" in report_dict
    assert "produto_mais_vendido" in report_dict
    assert "total_vendas_processadas" in report_dict

    assert report.total_per_product["Laptop"] == pytest.approx(
        (3500.50 * 2) + (3400.00 * 1)
    )
    assert report.total_per_product["Mouse"] == pytest.approx(
        (150.00 * 5) + (160.00 * 2)
    )
    assert report.total_per_product["Teclado"] == pytest.approx(300.25 * 3)
    assert report.total_per_product["Monitor"] == pytest.approx(800.00 * 1)
    assert report.total_per_product["Fone de ouvido"] == pytest.approx(200.00 * 4)

    expected_grand_total = sum(report.total_per_product.values())
    assert report.value_total_sales == pytest.approx(expected_grand_total)

    assert report.product_more_saled == ("Mouse", 7)
    assert report.total_sales_processed == 7


def test_generate_report_with_date_range_filter(service, sales_data):
    """testa se a filtragem esta correta"""
    start_date = date(2025, 10, 21)
    end_date = date(2025, 10, 22)

    report = service.generate_report(
        sales=sales_data,
        start_date=start_date,
        end_date=end_date,
    )

    assert report.total_sales_processed == 4
    assert "Fone de ouvido" not in report.total_per_product
    assert report.total_per_product["Mouse"] == pytest.approx(150.00 * 5)
    assert report.total_per_product["Teclado"] == pytest.approx(300.25 * 3)
    assert report.total_per_product["Monitor"] == pytest.approx(800.00 * 1)
    assert report.total_per_product["Laptop"] == pytest.approx(3400.00 * 1)
    assert report.product_more_saled == ("Mouse", 5)


def test_generate_report_empty_sales(service):
    """Testa no caso de dados vazios"""
    report = service.generate_report([])
    assert report.total_sales_processed == 0
    assert report.value_total_sales == 0.0
    assert report.product_more_saled is None
    assert report.total_per_product == {}


def test_find_best_selling_product_tie(service):
    """Testa um cenário de empate"""
    tied_sales = [
        Sale("A", 10, 5, date(2025, 1, 1)),
        Sale("B", 10, 5, date(2025, 1, 1)),
        Sale("C", 10, 3, date(2025, 1, 1)),
    ]
    report = service.generate_report(tied_sales)
    assert isinstance(report, Report)
    assert report.product_more_saled in [("A", 5), ("B", 5)]
