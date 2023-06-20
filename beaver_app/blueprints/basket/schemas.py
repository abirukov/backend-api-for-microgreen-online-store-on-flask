import marshmallow_dataclass
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from beaver_app.blueprints.basket.classes import BasketProductData, BasketUpdate
from beaver_app.blueprints.basket.models import BasketProduct
from beaver_app.blueprints.basket.models.basket import Basket
from beaver_app.blueprints.schemas import PaginationSchema
from beaver_app.db.db import db_session


class BasketProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db_session
        model = BasketProduct
        include_relationships = True
        load_instance = True
        include_fk = True
        transient = True

    basket_id = auto_field(dump_only=True)
    product_id = auto_field(dump_only=True)
    quantity = auto_field(dump_only=True)


class BasketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Basket
        include_relationships = True
        load_instance = True
        include_fk = True

    basket_products = Nested(BasketProductSchema, many=True)


class BasketsListResponseSchema(Schema):
    result = fields.List(fields.Nested(BasketSchema()))
    pagination = fields.Nested(PaginationSchema())


BasketProductDataSchema = marshmallow_dataclass.class_schema(BasketProductData)
BasketUpdateSchema = marshmallow_dataclass.class_schema(BasketUpdate)
