from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from beaver_app.db.base import Base

if TYPE_CHECKING:
    from beaver_app.blueprints.category.models.category import Category
    from beaver_app.blueprints.product.models.product import Product


class ProductCategory(Base):
    __tablename__ = "product_categories"
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())
    products: Mapped["Product"] = relationship(back_populates="categories")
    categories: Mapped["Category"] = relationship(back_populates="products")
