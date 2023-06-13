from marshmallow import fields, Schema

from beaver_app.blueprints.basket.models.basket import Basket
from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema


class BasketSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Basket
        include_relationships = True
        load_instance = True
        include_fk = True


class BasketsListResponseSchema(Schema):
    result = fields.List(fields.Nested(BasketSchema()))
    pagination = fields.Nested(PaginationSchema())


class BasketProductData(Schema):
    product_id = fields.String()
    quantity = fields.Float()


class BasketUpdateSchema(Schema):
    add = fields.List(fields.Nested(BasketProductData()))
    remove = fields.List(fields.Nested(BasketProductData()))
