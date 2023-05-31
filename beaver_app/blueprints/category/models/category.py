import uuid
from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from beaver_app.blueprints.product.models.product import Product

from beaver_app.db.enums import SqlAlchemyFiltersOperands


class Category(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'categories'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    products: Mapped[List['Product']] = relationship(back_populates='category')

    @staticmethod
    def get_search_params(search_value: str) -> dict:
        fields = ['title']
        list_result: dict = {'or': []}
        for field in fields:
            list_result['or'].append({
                'field': field,
                'op': SqlAlchemyFiltersOperands.ILIKE.value,
                'value': f'%{search_value}%',
            })
        return list_result
