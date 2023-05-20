from enum import Enum

from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.product.models import Product


class Entities(Enum):
    PRODUCT = Product
    CATEGORY = Category
