import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from beaver_app.db.base import Base

if TYPE_CHECKING:
    from beaver_app.blueprints.category.models.product_category import ProductCategory


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())
    categories: Mapped[List["ProductCategory"]] = relationship(back_populates="category")
