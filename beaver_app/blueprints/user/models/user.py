import uuid

from flask import current_app
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped
from werkzeug.security import generate_password_hash, check_password_hash

from beaver_app.blueprints.user.utils import generate_personal_code
from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin
from flask_jwt_extended import create_access_token
from datetime import timedelta
from typing import TypeVar

TypingUser = TypeVar('TypingUser', bound='User')


class User(Base, TimestampMixin, IsDeletedMixin):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(255))
    tg_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    tg_username: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    personal_code: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    inviter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=True,
    )

    def __init__(self, **kwargs):
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.middle_name = kwargs.get('middle_name')
        self.phone = kwargs.get('phone')
        self.email = kwargs.get('email')
        self.password = generate_password_hash(kwargs.get('password'))
        self.tg_id = kwargs.get('tg_id')
        self.tg_username = kwargs.get('tg_username')
        self.personal_code = self.get_personal_code()
        self.is_admin = False
        self.inviter_id = kwargs.get('inviter_id')

    def get_token(self) -> str:
        token = create_access_token(
            identity=self.id,
            expires_delta=timedelta(current_app.config['TOKEN_LIFETIME_IN_HOURS']),
        )
        return token

    def get_personal_code(self) -> str:
        personal_code = generate_personal_code()
        while self.is_personal_code_uniq(personal_code) is False:
            personal_code = generate_personal_code()
        return personal_code

    @classmethod
    def is_personal_code_uniq(cls, personal_code: str) -> bool:
        user = cls.query.filter(cls.personal_code == personal_code).first()
        return user is None

    @classmethod
    def authenticate_by_mail(cls, email: str, password: str) -> TypingUser | None:
        user = cls.query.filter(cls.email == email).first()
        if user is None or not check_password_hash(user.password, password):
            return None
        return user

    def __repr__(self):
        return '<User {}>'.format(self.email)
