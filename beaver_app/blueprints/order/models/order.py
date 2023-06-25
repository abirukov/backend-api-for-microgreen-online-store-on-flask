import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from beaver_app.blueprints.user.models.user import User

if TYPE_CHECKING:
    from beaver_app.blueprints.product.models.product import Product
    from beaver_app.blueprints.order.models.order_product import OrderProduct


class Order(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'orders'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)
    status: Mapped[str] = mapped_column(String())
    address: Mapped[str] = mapped_column(Text())
    comment: Mapped[str] = mapped_column(Text())
    total: Mapped[float] = mapped_column(Float())

    products: Mapped[List['Product']] = relationship(secondary='order_products', back_populates='orders')
    user: Mapped['User'] = relationship(back_populates='order')
    order_products: Mapped[List['OrderProduct']] = relationship(
        back_populates='order',
        overlaps='products',
    )

    @staticmethod
    def get_search_fields() -> list:
        return ['comment', 'address', 'status']
