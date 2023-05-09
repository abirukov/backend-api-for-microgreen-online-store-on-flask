import uuid

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from beaver_app.models import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    phone = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    tg_id = db.Column(db.String(255), unique=True)
    tg_username = db.Column(db.String(255))
    discount_code = db.Column(db.String(255))
    is_admin_col = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    from_user_id = db.Column(UUID(as_uuid=True))
    personal_price_mode = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        return self.is_admin_col

    def __repr__(self):
        return '<User {}>'.format(self.username)
