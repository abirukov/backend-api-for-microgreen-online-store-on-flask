import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from beaver_app.db.base import Base
from beaver_app.db.mixin import TimestampMixin

if TYPE_CHECKING:
    from beaver_app.blueprints.category.models.category import Category


class Product(TimestampMixin, Base):
    __tablename__ = "products"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())
    description: Mapped[str] = mapped_column(Text())
    category_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    category: Mapped["Category"] = relationship(back_populates="product")
