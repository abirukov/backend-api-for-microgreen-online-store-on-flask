import random
import string
import uuid

from beaver_app.db.db_utils import is_entity_exist_by_field
from beaver_app.enums import Entities


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
    return not is_entity_exist_by_field(Entities.USER, 'personal_code', personal_code)
