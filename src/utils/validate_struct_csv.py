from typing import List

REQUIRED_COLUMNS = ["produto", "quantidade", "preco_unitario"]
OPTIONAL_COLUMNS = ["data"]


def validate_columns_csv(columns: List[str]) -> bool:
    """Valida se as colunas do CSV estão de acordo com o padrão estabelecido.

    Args:
        columns: Uma lista de strings com os nomes das colunas do CSV.

    Returns:
        True se as colunas obrigatórias estiverem presentes, False caso contrário.
    """
    given_columns = set(columns)
    
    # Verifica se todas as colunas obrigatórias estão presentes
    if not set(REQUIRED_COLUMNS).issubset(given_columns):
        return False
    
    # Garante que não há colunas inesperadas (além das opcionais)
    allowed_columns = set(REQUIRED_COLUMNS + OPTIONAL_COLUMNS)
    if not given_columns.issubset(allowed_columns):
        # Se quiser ser mais restritivo e não permitir colunas extras
        # return False
        pass  # Atualmente, permite colunas extras não utilizadas

    return True
