import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from beaver_app.blueprints.user.models.user import User
from beaver_app.blueprints.basket.models.basket_product import BasketProduct

if TYPE_CHECKING:
    from beaver_app.blueprints.product.models.product import Product


class Basket(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'baskets'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)

    products: Mapped[List['Product']] = relationship(secondary='basket_products', back_populates='baskets')
    user: Mapped['User'] = relationship(back_populates='basket')
    basket_products: Mapped[List['BasketProduct']] = relationship(back_populates='basket')
