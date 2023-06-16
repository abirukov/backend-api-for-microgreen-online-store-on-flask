from beaver_app.blueprints.basket.enums import RecordTypeUpdateBasket
from beaver_app.blueprints.basket.models import Basket, BasketProduct
from beaver_app.blueprints.product.classes.product_update_row import ProductUpdateRow
from beaver_app.blueprints.product.models import Product
from beaver_app.db.db_utils import save
from beaver_app.db.db import db_session


def update_products_in_basket(basket: Basket, products_data: dict) -> None:
    handle_record_type(RecordTypeUpdateBasket.ADD, basket, products_data)
    handle_record_type(RecordTypeUpdateBasket.REMOVE, basket, products_data)
    db_session.commit()


def handle_record_type(record_type: RecordTypeUpdateBasket, basket: Basket, products_data: dict) -> None:
    if record_type.value not in products_data:
        return
    for product_row in products_data[record_type.value]:
        product_update_row = ProductUpdateRow(product_row['product_id'], product_row['quantity'])
        if record_type == RecordTypeUpdateBasket.ADD:
            add_product(basket, product_update_row)
        else:
            remove_product(basket, product_update_row)


def add_product(basket: Basket, product_row: ProductUpdateRow) -> None:
    product_row_in_basket = list(filter(
        lambda product_r: str(product_r.product_id) == product_row.product_id,
        basket.basket_products,
    ))
    if not product_row_in_basket:
        product = Product.query.filter_by(id=product_row.product_id).first()
        if product is None:
            raise Exception(f'not found product with id = {product_row.product_id}')
        save(BasketProduct(
            basket_id=basket.id,
            product_id=product.id,
            quantity=product_row.quantity,
        ))
    else:
        product_row_in_basket[0].quantity += float(product_row.quantity)


def remove_product(basket: Basket, product_row: ProductUpdateRow) -> None:
    product_row_in_basket = list(filter(
        lambda product_r: str(product_r.product_id) == product_row.product_id,
        basket.basket_products,
    ))
    if product_row_in_basket is None:
        raise Exception(f'not found in basket(id={basket.id}) with product (id = {product_row.product_id})')
    elif product_row_in_basket[0].quantity > float(product_row.quantity):
        product_row_in_basket[0].quantity -= float(product_row.quantity)
    else:
        product = Product.query.filter_by(id=product_row.product_id).first()
        basket.products.remove(product)
