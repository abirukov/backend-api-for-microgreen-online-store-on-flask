import uuid
from datetime import datetime
from typing import List

from sqlalchemy import String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from beaver_app.blueprints.category.models.product_category import ProductCategory


class Category(DeclarativeBase):
    __tablename__ = "products"
    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())
    categories: Mapped[List[ProductCategory]] = relationship(back_populates="category")