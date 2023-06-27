from beaver_app.blueprints.order.models import OrderProduct
from beaver_app.db.db import db_session
from beaver_app.db.db_utils import get_by_id, delete
from beaver_app.enums import Entities


def test__orders_view__list_admin(client, admin_auth_headers, order_list):
    response = client.get('/orders', follow_redirects=True, headers=admin_auth_headers)
    response_ids = [r_order['id'] for r_order in response.json['result']]
    assert response_ids == [str(order.id) for order in order_list]


def test__orders_view__list_client(client, first_client_auth_headers, order_first, order_list):  # noqa: U100
    response = client.get('/orders', follow_redirects=True, headers=first_client_auth_headers)
    assert response.json['result'][0]['id'] == str(order_first.id)


def test__orders_view__list_no_auth(client):
    response = client.get('/orders', follow_redirects=True)
    assert response.json == {'msg': 'Missing Authorization Header'}


def test__orders_view__create_success(client, first_client_auth_headers, basket_product):
    order_data = {
        'address': 'Адрес тест',
        'comment': 'Коммент тест',
    }
    response = client.post(
        '/orders',
        json=order_data,
        headers=first_client_auth_headers,
        follow_redirects=True
    )
    response_dict = response.json
    print(f'111111{response.json}')

    assert order_data['address'] == response_dict['address']
    assert basket_product.quantity * basket_product.product.price == response_dict['total']
    assert basket_product.quantity == response_dict['order_products'][0]['quantity']
    assert basket_product.product.price == response_dict['order_products'][0]['unit_price']

    OrderProduct.query.filter_by(
        order_id=response_dict['id'],
        product_id=basket_product.product.id,
    ).delete()
    db_session.commit()
    order = get_by_id(Entities.ORDER, response_dict['id'])
    delete(order)


def test__orders_view__create_fail_unauthorized(client):
    order_data = {}
    response = client.post('/orders', json=order_data, follow_redirects=True)

    assert response.status_code == 401
