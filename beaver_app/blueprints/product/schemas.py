from dataclasses import field, dataclass

import marshmallow_dataclass
from marshmallow import Schema, fields, validate

from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilter


class ProductSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Product
        include_relationships = True
        load_instance = True
        include_fk = True


@dataclass
class ProductsGetListFilter(BaseGetListFilter):
    title: str | None = None
    price: float | None = None
    description: str | None = None
    category_id: str | None = None
    price_less: float | None = None
    price_more: float | None = None
    sort_by_title: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )


ProductsGetListFilterSchema = marshmallow_dataclass.class_schema(BaseGetListFilter)


class ProductsListResponseSchema(Schema):
    result = fields.List(fields.Nested(ProductSchema()))
    pagination = fields.Nested(PaginationSchema())
