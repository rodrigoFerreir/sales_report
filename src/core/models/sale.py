from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Sale:
    product: str
    price: Decimal
    quantity: int
    data: Optional[date] = None
