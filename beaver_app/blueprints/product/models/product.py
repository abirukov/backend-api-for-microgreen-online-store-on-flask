import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from beaver_app.blueprints.category.models.category import Category

from beaver_app.blueprints.order.models.order_product import OrderProduct
from beaver_app.blueprints.basket.models.basket_product import BasketProduct

if TYPE_CHECKING:
    from beaver_app.blueprints.order.models.order import Order
    from beaver_app.blueprints.basket.models.basket import Basket


class Product(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'products'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())
    description: Mapped[str] = mapped_column(Text())
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('categories.id'),
        primary_key=True,
    )

    category: Mapped['Category'] = relationship(back_populates='products')
    baskets: Mapped[List['Basket']] = relationship(
        secondary='basket_products',
        back_populates='products',
        overlaps='basket_products',
    )
    product_baskets: Mapped[List['BasketProduct']] = relationship(back_populates='product', overlaps='baskets,products')

    orders: Mapped[List['Order']] = relationship(
        secondary='order_products',
        back_populates='products',
        overlaps='order_products',
    )
    product_orders: Mapped[List['OrderProduct']] = relationship(back_populates='product', overlaps='orders,products')

    @staticmethod
    def get_search_fields() -> list:
        return ['title', 'description']
