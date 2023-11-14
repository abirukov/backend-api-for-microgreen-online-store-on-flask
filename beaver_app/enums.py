from enum import Enum

from beaver_app.blueprints.basket.models.basket import Basket
from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.user.models.user import User
from beaver_app.blueprints.order.models.order import Order


class Entities(Enum):
    PRODUCT = Product
    CATEGORY = Category
    USER = User
    BASKET = Basket
    ORDER = Order
