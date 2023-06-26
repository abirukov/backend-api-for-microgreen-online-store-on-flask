from dataclasses import dataclass, field
import marshmallow_dataclass

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, validate
from beaver_app.db.db import db_session


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db_session


class PaginationSchema(Schema):
    page_number = fields.Integer()
    page_size = fields.Integer()
    num_pages = fields.Integer()
    total_results = fields.Integer()


@dataclass
class BaseGetListFilter:
    search: str | None = None
    id: str | None = None
    is_deleted: bool | None = None
    created_at: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    updated_at: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    created_at_before: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    updated_at_before: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    created_at_after: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    updated_at_after: str | None = field(default=None, metadata={'created_at': fields.DateTime()})
    sort_by_is_deleted: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    sort_by_created_at: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    sort_by_updated_at: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    page_number: int | None = None
    page_size: int | None = None


BaseGetListFilterSchema = marshmallow_dataclass.class_schema(BaseGetListFilter)
