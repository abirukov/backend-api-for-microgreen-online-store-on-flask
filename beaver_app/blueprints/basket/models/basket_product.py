import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from beaver_app.blueprints.models import BaseModel
from beaver_app.db.mixin import TimestampMixin

if TYPE_CHECKING:
    from beaver_app.blueprints.product.models.product import Product
    from beaver_app.blueprints.basket.models.basket import Basket


class BasketProduct(BaseModel, TimestampMixin):
    __tablename__ = 'basket_products'
    basket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('baskets.id'), primary_key=True)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('products.id'), primary_key=True)
    quantity: Mapped[float]

    basket: Mapped['Basket'] = relationship(back_populates='basket_products')
    product: Mapped['Product'] = relationship(back_populates='product_baskets')
