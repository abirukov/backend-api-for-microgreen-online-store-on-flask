from beaver_app.db.db_utils import get_by_id, delete
from beaver_app.enums import Entities


def test__products_view__list(client, product_list):
    response = client.get('/products', follow_redirects=True)
    count_entries = 0
    response_ids = [r_product['id'] for r_product in response.json['result']]
    for product in product_list:
        if str(product.id) in response_ids:
            count_entries += 1

    assert count_entries == len(product_list)


def test__products_view__create_success(client, saved_category):
    product_data = {
        'title': 'Товар тест',
        'price': '120.0',
        'description': 'Товар тест описание',
        'category_id': saved_category.id,
    }
    response = client.post('/products', json=product_data, follow_redirects=True)
    response_dict = response.json

    assert product_data['title'] == response_dict['title']

    product = get_by_id(Entities.PRODUCT, response_dict['id'])
    delete(product)


def test__products_view__create_fail_not_existing_field(client, saved_category):
    product_data = {
        'some_field': 'some_value',
        'title': 'Товар тест',
        'price': '120.0',
        'description': 'Товар тест описание',
        'category_id': str(saved_category.id),
    }
    response = client.post('/products', json=product_data, follow_redirects=True)

    assert response.status_code == 422


def test__products_view__create_fail_missing_field(client):
    product_data = {
        'title': 'Товар тест',
        'price': '120.0',
        'description': 'Товар тест описание',
    }
    response = client.post('/products', json=product_data, follow_redirects=True)

    assert response.status_code == 422


def test__products_view__get_success(client, saved_product):
    response = client.get(f'/products/{saved_product.id}', follow_redirects=True)
    response_dict = response.json

    assert str(saved_product.id) == response_dict['id']


def test__products_view__get_fail(client, not_existing_uuid):
    response = client.get(f'/products/{not_existing_uuid}', follow_redirects=True)

    assert response.status_code == 404


def test__products_view__update_success(client, saved_category, saved_product):
    new_product_data = {
        'title': 'title',
        'price': '120.0',
        'description': 'Товар тест описание',
        'category_id': saved_category.id,
    }
    response = client.put(f'/products/{saved_product.id}', json=new_product_data, follow_redirects=True)
    response_dict = response.json

    assert response_dict['title'] == 'title'


def test__products_view__update_fail_missing_field(client, saved_product):
    new_product_data = {'title': 'title'}
    response = client.put(f'/products/{saved_product.id}', json=new_product_data, follow_redirects=True)

    assert response.status_code == 422


def test__products_view__update_fail_not_existing_uuid(client, saved_category, not_existing_uuid):
    new_product_data = {
        'title': 'title',
        'price': '120.0',
        'description': 'Товар тест описание',
        'category_id': saved_category.id,
    }
    response = client.put(f'/products/{not_existing_uuid}', json=new_product_data, follow_redirects=True)

    assert response.status_code == 404


def test__products_view__delete_success(client, saved_product):
    response = client.delete(f'/products/{saved_product.id}', follow_redirects=True)
    response_dict = response.json
    product_in_db = get_by_id(Entities.PRODUCT, saved_product.id)

    assert response_dict == {}
    assert product_in_db.is_deleted is True


def test__products_view__delete_fail(client, not_existing_uuid):
    response = client.delete(f'/products/{not_existing_uuid}', follow_redirects=True)

    assert response.status_code == 404
