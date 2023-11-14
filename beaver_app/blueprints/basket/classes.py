from typing import List
from dataclasses import dataclass


@dataclass
class BasketProductData:
    product_id: str
    quantity: int


@dataclass
class BasketUpdate:
    add: List[BasketProductData] | None
    remove: List[BasketProductData] | None
