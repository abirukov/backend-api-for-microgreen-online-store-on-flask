from marshmallow import Schema, fields, validate

from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilterSchema


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category
        include_relationships = True
        load_instance = True


class CategoryGetListFilterSchema(BaseGetListFilterSchema):
    title = fields.String()
    sort_by_title = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)


class CategoryListResponseSchema(Schema):
    result = fields.List(fields.Nested(CategorySchema()))
    pagination = fields.Nested(PaginationSchema())
