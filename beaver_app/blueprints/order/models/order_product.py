import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin


from beaver_app.blueprints.product.models.product import Product
from beaver_app.blueprints.order.models.order import Order


class OrderProduct(Base, TimestampMixin):
    __tablename__ = 'order_products'
    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('orders.id'),
        primary_key=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True,
    )
    quantity: Mapped[int]

    order: Mapped['Order'] = relationship(
        back_populates='order_products',
        overlaps='orders,products',
    )
    product: Mapped['Product'] = relationship(
        back_populates='product_orders',
        overlaps='orders,products',
    )
