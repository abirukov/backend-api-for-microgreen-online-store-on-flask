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


def test__orders_view__create_success(client, first_client_auth_headers, basket_product):  # noqa: U100
    order_data = {
        'address': 'Адрес тест',
        'comment': 'Коммент тест',
    }
    response = client.post(
        '/orders',
        json=order_data,
        headers=first_client_auth_headers,
        follow_redirects=True,
    )
    response_dict = response.json
    order = get_by_id(Entities.ORDER, response_dict['id'])
    order_product = order.order_products[0]

    assert order_data['address'] == response_dict['address']
    assert order_product.quantity * order_product.product.price == response_dict['total']
    assert order_product.quantity == response_dict['order_products'][0]['quantity']
    assert order_product.product.price == response_dict['order_products'][0]['unit_price']

    OrderProduct.query.filter_by(
        order_id=response_dict['id'],
    ).delete()
    db_session.commit()
    delete(order)


def test__orders_view__create_fail_unauthorized(client):
    order_data = {}
    response = client.post('/orders', json=order_data, follow_redirects=True)

    assert response.status_code == 401


def test__orders_view__get_success(client, order_first, first_client_auth_headers):
    response = client.get(
        f'/orders/{order_first.id}',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )
    response_dict = response.json

    assert str(order_first.id) == response_dict['id']


def test__orders_view__get_fail_another_user(client, order_second, first_client_auth_headers):
    response = client.get(
        f'/orders/{order_second.id}',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 403


def test__orders_view__get_fail_not_existing_uuid(client, first_client_auth_headers, not_existing_uuid):
    response = client.get(
        f'/orders/{not_existing_uuid}',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 404


def test__orders_view__get_fail_no_auth(client, order_first):
    response = client.get(
        f'/orders/{order_first.id}',
        follow_redirects=True,
    )

    assert response.status_code == 401


def test__orders_view__update_success(client, order_first, first_client_auth_headers):
    new_order_data = {
        'status': 'delivered',
        'address': 'Адрес тест обновления',
        'comment': 'Коммент тест обновления',
    }
    response = client.put(
        f'/orders/{order_first.id}',
        headers=first_client_auth_headers,
        json=new_order_data,
        follow_redirects=True,
    )
    response_dict = response.json

    assert response_dict['status'] == new_order_data['status']
    assert response_dict['address'] == new_order_data['address']
    assert response_dict['comment'] == new_order_data['comment']


def test__orders_view__update_fail_another_user(client, order_second, first_client_auth_headers):
    new_order_data = {
        'status': 'delivered',
        'address': 'Адрес тест обновления',
        'comment': 'Коммент тест обновления',
    }
    response = client.put(
        f'/orders/{order_second.id}',
        headers=first_client_auth_headers,
        json=new_order_data,
        follow_redirects=True,
    )

    assert response.status_code == 403


def test__orders_view__update_fail_not_existing_uuid(client, not_existing_uuid, first_client_auth_headers):
    new_order_data = {
        'status': 'delivered',
        'address': 'Адрес тест обновления',
        'comment': 'Коммент тест обновления',
    }
    response = client.put(
        f'/orders/{not_existing_uuid}',
        headers=first_client_auth_headers,
        json=new_order_data,
        follow_redirects=True,
    )

    assert response.status_code == 404
