from dataclasses import dataclass


@dataclass(frozen=True)
class ProductUpdateRow:
    product_id: str
    quantity: float
