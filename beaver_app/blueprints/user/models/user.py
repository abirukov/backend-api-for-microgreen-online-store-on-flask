import uuid

from flask import current_app
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from werkzeug.security import check_password_hash

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin, IsDeletedMixin

from flask_jwt_extended import create_access_token
from datetime import timedelta
from typing import TypeVar, TYPE_CHECKING
if TYPE_CHECKING:
    from beaver_app.blueprints.basket.models.basket import Basket

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
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=True)
    inviter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=True,
    )

    basket: Mapped['Basket'] = relationship(back_populates='user')

    def create_token(self) -> str:
        token = create_access_token(
            identity=self.id,
            expires_delta=timedelta(current_app.config['TOKEN_LIFETIME_IN_HOURS']),
        )
        return token

    @classmethod
    def authenticate_by_mail(cls, email: str, password: str) -> TypingUser | None:
        user = cls.query.filter(cls.email == email).first()
        if user is None or not check_password_hash(user.password, password):
            return None
        return user

    @classmethod
    def is_admin_by_id(cls, jwt_user_id: uuid.UUID) -> bool:
        user = cls.query.filter(cls.id == jwt_user_id).first()
        if user:
            return user.is_admin
        return False

    @staticmethod
    def get_search_fields() -> list:
        return [
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'email',
            'tg_id',
            'tg_username',
            'personal_code',
        ]

    @staticmethod
    def get_unique_fields() -> list[str]:
        return ['phone', 'email', 'tg_id']
