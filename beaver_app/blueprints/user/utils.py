import random
import string
import uuid

from beaver_app.blueprints.user.models import User
from beaver_app.db.db import db_session


def is_current_user(jwt_user_id: str, checked_user_id: uuid.UUID) -> bool:
    return jwt_user_id == str(checked_user_id)


def get_personal_code() -> str:
    personal_code = generate_personal_code()
    while is_personal_code_uniq(personal_code) is False:
        personal_code = generate_personal_code()
    return personal_code


def generate_personal_code() -> str:
    chars = [random.choice(string.ascii_uppercase) for _ in range(2)]
    numbers = [random.choice(string.digits) for _ in range(2)]
    return ''.join(chars + numbers)


def is_personal_code_uniq(personal_code: str) -> bool:
    return not db_session.query(
        User.query.filter(User.personal_code == personal_code).exists(),
    ).first()[0]
