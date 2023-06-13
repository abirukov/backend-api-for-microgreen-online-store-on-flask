from marshmallow import fields, Schema, validate

from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilterSchema
from beaver_app.blueprints.user.models.user import User


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True


class UsersGetListFilterSchema(BaseGetListFilterSchema):
    first_name = fields.String()
    last_name = fields.String()
    middle_name = fields.String()
    phone = fields.String()
    email = fields.String()
    tg_id = fields.String()
    tg_username = fields.String()
    personal_code = fields.String()
    is_admin = fields.Boolean()
    inviter_id = fields.String()
    sort_by_first_name = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    sort_by_last_name = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    sort_by_middle_name = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)
    sort_by_inviter_id = fields.String(validate=validate.OneOf(('asc', 'desc')), allow_none=True)


class UsersListResponseSchema(Schema):
    result = fields.List(fields.Nested(UserSchema()))
    pagination = fields.Nested(PaginationSchema())


class UserLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
