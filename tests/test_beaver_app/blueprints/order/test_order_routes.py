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
