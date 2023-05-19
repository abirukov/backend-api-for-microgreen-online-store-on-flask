import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from beaver_app.db.base import Base
from beaver_app.db.mixin import TimestampMixin

if TYPE_CHECKING:
    from beaver_app.blueprints.product.models.product import Product


class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    products: Mapped[List["Product"]] = relationship(back_populates="category")
