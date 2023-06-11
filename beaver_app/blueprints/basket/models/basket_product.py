import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin

if TYPE_CHECKING:
    from beaver_app.blueprints.product.models.product import Product
    from beaver_app.blueprints.basket.models.basket import Basket


class BasketProduct(Base, TimestampMixin):
    __tablename__ = 'basket_products'
    basket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('baskets.id'), primary_key=True)
    basket: Mapped['Basket'] = relationship(back_populates='basket')
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('products.id'), primary_key=True)
    product: Mapped['Product'] = relationship(back_populates='product')
    quantity: Mapped[float]

    @staticmethod
    def get_search_fields() -> list:
        return []
