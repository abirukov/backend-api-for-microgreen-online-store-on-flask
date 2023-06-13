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


class BaseGetListFilterSchema(Schema):
    search = fields.String()
    id = fields.String()
    is_deleted = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    created_at_before = fields.DateTime()
    updated_at_before = fields.DateTime()
    created_at_after = fields.DateTime()
    updated_at_after = fields.DateTime()
    sort_by_is_deleted = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    sort_by_created_at = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    sort_by_updated_at = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    page_number = fields.Integer()
    page_size = fields.Integer()
