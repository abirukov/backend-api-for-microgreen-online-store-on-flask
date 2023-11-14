from dataclasses import field, dataclass

import marshmallow_dataclass
from marshmallow import Schema, fields, validate

from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilter


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category
        include_relationships = True
        load_instance = True


@dataclass
class CategoryGetListFilter(BaseGetListFilter):
    title: str | None = None
    sort_by_title: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )


CategoryGetListFilterSchema = marshmallow_dataclass.class_schema(CategoryGetListFilter)


class CategoryListResponseSchema(Schema):
    result = fields.List(fields.Nested(CategorySchema()))
    pagination = fields.Nested(PaginationSchema())
