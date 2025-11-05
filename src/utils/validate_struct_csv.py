from typing import List

REQUIRED_COLUMNS = ["produto", "quantidade", "preco_unitario"]
OPTIONAL_COLUMNS = ["data"]


def validate_columns_csv(columns: List[str]) -> bool:
    """Valida se as colunas do CSV estão de acordo com o padrão estabelecido.

    Verifica se todas as colunas obrigatórias estão presentes e se não há colunas inesperadas.

    Args:
        columns (List[str]): Uma lista de strings com os nomes das colunas do CSV.

    Returns:
        bool: True se as colunas obrigatórias estiverem presentes e não houver colunas inesperadas, False caso contrário.
    """
    given_columns = set(columns)

    # Verifica se todas as colunas obrigatórias estão presentes
    if not set(REQUIRED_COLUMNS).issubset(given_columns):
        return False

    # Garante que não há colunas inesperadas (além das opcionais)
    allowed_columns = set(REQUIRED_COLUMNS + OPTIONAL_COLUMNS)
    if not given_columns.issubset(allowed_columns):
        pass

    return True
