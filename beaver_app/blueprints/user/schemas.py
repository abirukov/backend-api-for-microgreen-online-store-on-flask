from dataclasses import dataclass, field

import marshmallow_dataclass
from marshmallow import fields, Schema, validate

from beaver_app.blueprints.schemas import BaseSchema, PaginationSchema, BaseGetListFilter
from beaver_app.blueprints.user.models.user import User


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True


@dataclass
class UsersGetListFilter(BaseGetListFilter):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: str | None = None
    email: str | None = None
    tg_id: str | None = None
    tg_username: str | None = None
    personal_code: str | None = None
    is_admin: bool | None = None
    inviter_id: str | None = None
    sort_by_first_name: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    sort_by_last_name: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    sort_by_middle_name: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )
    sort_by_inviter_id: str | None = field(
        default=None,
        metadata={'validate': validate.OneOf(('asc', 'desc'))},
    )


UsersGetListFilterSchema = marshmallow_dataclass.class_schema(UsersGetListFilter)


class UserDataWithTokenSchema(Schema):
    user_data = fields.Nested(UserSchema())
    access_token = fields.String()


class UsersListResponseSchema(Schema):
    result = fields.List(fields.Nested(UserSchema()))
    pagination = fields.Nested(PaginationSchema())


@dataclass
class UserLogin:
    email: str
    password: str


UserLoginSchema = marshmallow_dataclass.class_schema(UserLogin)
