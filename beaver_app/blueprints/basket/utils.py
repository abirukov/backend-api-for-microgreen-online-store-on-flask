from beaver_app.blueprints.basket.classes import BasketUpdate, BasketProductData
from beaver_app.blueprints.basket.enums import RecordTypeUpdateBasket
from beaver_app.blueprints.basket.models import Basket, BasketProduct
from beaver_app.blueprints.product.models import Product
from beaver_app.db.db_utils import save
from beaver_app.db.db import db_session


def update_products_in_basket(basket: Basket, products_data: BasketUpdate) -> None:
    handle_record_type(RecordTypeUpdateBasket.ADD, basket, products_data)
    handle_record_type(RecordTypeUpdateBasket.REMOVE, basket, products_data)
    db_session.commit()


def handle_record_type(record_type: RecordTypeUpdateBasket, basket: Basket, products_data: BasketUpdate) -> None:
    if not hasattr(products_data, record_type.value) or getattr(products_data, record_type.value) is None:
        return
    for product_row in getattr(products_data, record_type.value):
        basket_product_data = BasketProductData(product_row.product_id, product_row.quantity)
        if record_type == RecordTypeUpdateBasket.ADD:
            add_product(basket, basket_product_data)
        else:
            remove_product(basket, basket_product_data)


def add_product(basket: Basket, basket_product_data: BasketProductData) -> None:
    product_row_in_basket = list(filter(
        lambda product_r: str(product_r.product_id) == basket_product_data.product_id,
        basket.basket_products,
    ))
    if not product_row_in_basket:
        product = Product.query.filter_by(id=basket_product_data.product_id).first()
        if product is None:
            raise Exception(f'not found product with id = {basket_product_data.product_id}')
        save(BasketProduct(
            basket_id=basket.id,
            product_id=product.id,
            quantity=basket_product_data.quantity,
        ))
    else:
        product_row_in_basket[0].quantity += basket_product_data.quantity


def remove_product(basket: Basket, basket_product_data: BasketProductData) -> None:
    product_row_in_basket = list(filter(
        lambda product_r: str(product_r.product_id) == basket_product_data.product_id,
        basket.basket_products,
    ))
    if product_row_in_basket is None:
        raise Exception(f'not found in basket(id={basket.id}) with product (id = {basket_product_data.product_id})')
    elif product_row_in_basket[0].quantity > basket_product_data.quantity:
        product_row_in_basket[0].quantity -= basket_product_data.quantity
    else:
        product = Product.query.filter_by(id=basket_product_data.product_id).first()
        basket.products.remove(product)
