import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from beaver_app.db.base import Base

if TYPE_CHECKING:
    from beaver_app.blueprints.category.models.product_category import ProductCategory


class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())
    description: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())
    categories: Mapped[List["ProductCategory"]] = relationship(back_populates="product")
