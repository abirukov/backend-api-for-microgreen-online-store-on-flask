def test__basket_view__list_success(client, admin_auth_headers, basket_list):
    response = client.get(
        '/baskets/list',
        headers=admin_auth_headers,
        follow_redirects=True,
    )
    response_ids = [r_basket['id'] for r_basket in response.json['result']]
    assert response_ids == [str(b.id) for b in basket_list]


def test__basket_view__list_fail(client, first_client_auth_headers):
    response = client.get(
        '/baskets/list',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )
    assert response.status_code == 403


def test__basket_view__get_success(client, first_client_auth_headers, basket):
    response = client.get(
        '/baskets',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )
    response_dict = response.json

    assert str(basket.id) == response_dict['id']


def test__basket_view__get_fail(client, admin_auth_headers):
    response = client.get(
        '/baskets',
        headers=admin_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 404


def test__basket_view__update_success(
    client,
    first_client_auth_headers,
    product,
    basket, # noqa U100
):
    new_product_data = {
        'add': [
            {'product_id': product.id, 'quantity': 5.0},
        ],
        'remove': [
            {'product_id': product.id, 'quantity': 3.0},
        ],
    }
    response = client.put(
        '/baskets/',
        headers=first_client_auth_headers,
        json=new_product_data,
        follow_redirects=True,
    )
    response_dict = response.json

    assert response_dict['basket_products'][0]['quantity'] == 2.0


def test__basket_view__update_fail_missing_field(client, first_client_auth_headers, basket): # noqa U100
    new_product_data = {'title': 'title'}
    response = client.put(
        '/baskets/',
        headers=first_client_auth_headers,
        json=new_product_data,
        follow_redirects=True,
    )

    assert response.status_code == 422


def test__basket_view__update_fail_no_found_basket(client, first_client_auth_headers, product):
    new_product_data = {
        'add': [
            {'product_id': product.id, 'quantity': 5.0},
        ],
        'remove': [
            {'product_id': product.id, 'quantity': 3.0},
        ],
    }
    response = client.put(
        '/baskets/',
        headers=first_client_auth_headers,
        json=new_product_data,
        follow_redirects=True,
    )

    assert response.status_code == 404
