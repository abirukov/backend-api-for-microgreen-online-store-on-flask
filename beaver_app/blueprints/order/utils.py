from beaver_app.blueprints.basket.models import Basket
from beaver_app.blueprints.order.models import Order, OrderProduct
from beaver_app.db.db_utils import save, update


def handle_basket(order: Order, basket: Basket) -> None:
    total = 0
    for basket_product in basket.basket_products:
        total += basket_product.quantity * basket_product.product.price
        save(OrderProduct(
            order_id=order.id,
            product_id=basket_product.product.id,
            quantity=basket_product.quantity,
            unit_price=basket_product.product.price,
        ))
    order.total = total
    update(order)
