from dataclasses import dataclass, field

import marshmallow_dataclass
from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from beaver_app.blueprints.order.models import OrderProduct
from beaver_app.blueprints.order.models.order import Order
from beaver_app.blueprints.schemas import PaginationSchema, BaseGetListFilter
from beaver_app.db.db import db_session


class OrderProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db_session
        model = OrderProduct
        include_relationships = True
        load_instance = True
        include_fk = True
        transient = True

    order_id = auto_field(dump_only=True)
    product_id = auto_field(dump_only=True)
    quantity = auto_field(dump_only=True)


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
        load_instance = True
        include_fk = True

    order_products = Nested(OrderProductSchema, many=True)


@dataclass
class OrdersGetListFilter(BaseGetListFilter):
    user_id: str | None = None
    total: float | None = None
    total_less: float | None = None
    total_more: float | None = None
    status: str | None = None
    sort_by_status: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )


OrdersGetListFilterSchema = marshmallow_dataclass.class_schema(OrdersGetListFilter)


class OrdersListResponseSchema(Schema):
    result = fields.List(fields.Nested(OrderSchema()))
    pagination = fields.Nested(PaginationSchema())
