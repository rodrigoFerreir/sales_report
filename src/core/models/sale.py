from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Sale:
    product: str
    price: float
    quantity: int
    data: Optional[date] = None
