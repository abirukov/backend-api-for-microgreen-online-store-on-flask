import uuid

from sqlalchemy import Integer, String, ForeignKey

from beaver_app.db.db import Base
from beaver_app.db.mixin import TimestampMixin
from sqlalchemy.orm import mapped_column, Mapped


class TokenBlocklist(Base, TimestampMixin):
    __tablename__ = 'token_blocklist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
