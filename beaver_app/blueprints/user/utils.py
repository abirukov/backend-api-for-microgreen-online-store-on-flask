import random
import string
import uuid


def is_current_user(jwt_user_id: uuid.UUID, checked_user_id: uuid.UUID) -> bool:
    return jwt_user_id == checked_user_id


def generate_personal_code() -> str:
    chars = [random.choice(string.ascii_uppercase) for _ in range(2)]
    numbers = [random.choice(string.digits) for _ in range(2)]
    return ''.join(chars + numbers)
