from typing import List
from dataclasses import dataclass


@dataclass
class BasketProductData:
    product_id: str
    quantity: float


@dataclass
class BasketUpdate:
    add: List[BasketProductData] | None
    remove: List[BasketProductData] | None
