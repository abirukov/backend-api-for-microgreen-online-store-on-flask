from enum import Enum

from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.user.models.user import User


class Entities(Enum):
    PRODUCT = Product
    CATEGORY = Category
    USER = User
