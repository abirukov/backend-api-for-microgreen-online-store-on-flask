import random
import string
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beaver_app.enums import Entities
    from beaver_app.db.db_utils import get_by_id


def is_current_user(jwt_user_id: uuid.UUID, checked_user_id: uuid.UUID) -> bool:
    return jwt_user_id == checked_user_id


def is_admin(jwt_user_id: uuid.UUID) -> bool:
    user = get_by_id(Entities.USER, jwt_user_id)
    if user:
        return user.is_admin
    return False


def generate_personal_code() -> str:
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(3)])
