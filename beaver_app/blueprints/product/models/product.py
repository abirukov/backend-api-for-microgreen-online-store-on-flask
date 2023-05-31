import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from beaver_app.db.enums import SqlAlchemyFiltersOperands

if TYPE_CHECKING:
    from beaver_app.blueprints.category.models.category import Category


class Product(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'products'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())
    description: Mapped[str] = mapped_column(Text())
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)
    category: Mapped['Category'] = relationship(back_populates='products')

    @staticmethod
    def get_search_params(search_value: str) -> dict:
        fields = ['title', 'description']
        list_result: dict = {'or': []}
        for field in fields:
            list_result['or'].append({
                'field': field,
                'op': SqlAlchemyFiltersOperands.ILIKE.value,
                'value': f'%{search_value}%',
            })
        return list_result
