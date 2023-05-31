from marshmallow import Schema, fields, validate

from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilterSchema


class ProductSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Product
        include_relationships = True
        load_instance = True
        include_fk = True


class ProductsGetListFilterSchema(BaseGetListFilterSchema):
    title = fields.String()
    price = fields.Float()
    description = fields.String()
    category_id = fields.String()
    price_less = fields.Float()
    price_more = fields.Float()
    sort_by_title = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)


class ProductsListResponseSchema(Schema):
    result = fields.List(fields.Nested(ProductSchema()))
    pagination = fields.Nested(PaginationSchema())
