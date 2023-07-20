from uuid import UUID

from beaver_app.blueprints.user.schemas import UsersGetListFilter
from beaver_app.db.db_utils import get_by_id, delete, get_list
from beaver_app.enums import Entities


def test__users_view__list_admin(client, admin_auth_headers, user_list):
    response = client.get('/users', follow_redirects=True, headers=admin_auth_headers)
    response_ids = [r_user['id'] for r_user in response.json['result']]
    for user in user_list:
        assert str(user.id) in response_ids


def test__users_view__list_client(client, first_client_auth_headers):
    response = client.get('/users', follow_redirects=True, headers=first_client_auth_headers)
    assert response.json == {'code': 403, 'status': 'Forbidden'}


def test__users_view__list_no_auth(client):
    response = client.get('/users', follow_redirects=True)
    assert response.json == {'msg': 'Missing Authorization Header'}


def test__users_view__create_success(client, user_admin, admin_auth_headers):
    user_data = {
        'first_name': 'test_create',
        'last_name': 'test_create',
        'middle_name': 'test_create',
        'phone': 'test_create',
        'email': 'test_create@test_create.ru',
        'password': 'test_create',
        'tg_id': '52525225255',
        'tg_username': 'test_create',
        'inviter_id': user_admin.id,
    }
    response = client.post(
        '/users',
        headers=admin_auth_headers,
        json=user_data,
        follow_redirects=True,
    )
    response_dict = response.json

    assert user_data['first_name'] == response_dict['first_name']
    assert user_data['last_name'] == response_dict['last_name']
    assert user_data['middle_name'] == response_dict['middle_name']
    assert user_data['phone'] == response_dict['phone']
    assert user_data['email'] == response_dict['email']
    assert user_data['tg_id'] == response_dict['tg_id']
    assert user_data['tg_username'] == response_dict['tg_username']
    assert user_data['inviter_id'] == UUID(response_dict['inviter_id'])

    user = get_by_id(Entities.USER, response_dict['id'])

    delete(user.basket)
    delete(user)


def test__users_view__create_fail_no_required_field(client, admin_auth_headers):
    user_data = {
        'first_name': 'second',
        'last_name': 'second',
        'middle_name': 'second',
        'phone': '79998887703',
    }
    response = client.post(
        '/users',
        headers=admin_auth_headers,
        json=user_data,
        follow_redirects=True,
    )
    assert response.status_code == 422


def test__users_view__create_fail_forbidden(client, user_client_first, first_client_auth_headers):
    user_data = {
        'first_name': 'test_create',
        'last_name': 'test_create',
        'middle_name': 'test_create',
        'phone': 'test_create',
        'email': 'test_create@test_create.ru',
        'password': 'test_create',
        'tg_id': '52525225255',
        'tg_username': 'test_create',
        'inviter_id': user_client_first.id,
    }
    response = client.post(
        '/users',
        headers=first_client_auth_headers,
        json=user_data,
        follow_redirects=True,
    )
    assert response.status_code == 403


def test__users_view__create_fail_duplicate_uniq_field(client, user_admin, admin_auth_headers):
    user_data = {
        'first_name': 'second',
        'last_name': 'second',
        'middle_name': 'second',
        'password': 'second',
        'phone': user_admin.phone,
    }
    response = client.post(
        '/users',
        headers=admin_auth_headers,
        json=user_data,
        follow_redirects=True,
    )
    assert response.status_code == 400


def test__users_view__get_success_admin(client, user_client_first, admin_auth_headers):
    response = client.get(
        f'/users/{user_client_first.id}',
        headers=admin_auth_headers,
        follow_redirects=True,
    )
    response_dict = response.json

    assert str(user_client_first.id) == response_dict['id']


def test__users_view__get_fail_no_no_auth(client, user_client_first):
    response = client.get(
        f'/users/{user_client_first.id}',
        follow_redirects=True,
    )

    assert response.status_code == 401


def test__users_view__get_success_client(client, user_client_first, first_client_auth_headers):
    response = client.get(
        f'/users/{user_client_first.id}',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )
    response_dict = response.json
    assert str(user_client_first.id) == response_dict['id']


def test__users_view__get_fail_client(client, user_client_second, first_client_auth_headers):
    response = client.get(
        f'/users/{user_client_second.id}',
        headers=first_client_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 403


def test__users_view__get_fail_no_user(client, not_existing_uuid, admin_auth_headers):
    response = client.get(
        f'/users/{not_existing_uuid}',
        headers=admin_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 404


def test__users_view__update_success_admin(client, user_client_first, admin_auth_headers):
    new_user_data = {
        'first_name': 'first_name_test',
        'last_name': user_client_first.last_name,
        'middle_name': user_client_first.middle_name,
        'phone': user_client_first.phone,
        'email': user_client_first.email,
        'password': user_client_first.password,
    }
    response = client.put(
        f'/users/{user_client_first.id}',
        headers=admin_auth_headers,
        json=new_user_data,
        follow_redirects=True,
    )
    response_dict = response.json

    assert str(user_client_first.id) == response_dict['id']


def test__users_view__update_fail_no_auth(client, user_client_first):
    new_user_data = {
        'first_name': 'first_name_test',
        'last_name': user_client_first.last_name,
        'middle_name': user_client_first.middle_name,
        'phone': user_client_first.phone,
        'email': user_client_first.email,
        'password': user_client_first.password,
    }
    response = client.put(
        f'/users/{user_client_first.id}',
        json=new_user_data,
        follow_redirects=True,
    )
    assert response.status_code == 401


def test__users_view__update_success_client(client, user_client_first, first_client_auth_headers):
    new_user_data = {
        'first_name': 'first_name_test_client',
        'last_name': user_client_first.last_name,
        'middle_name': user_client_first.middle_name,
        'phone': user_client_first.phone,
        'email': user_client_first.email,
        'password': user_client_first.password,
    }
    response = client.put(
        f'/users/{user_client_first.id}',
        headers=first_client_auth_headers,
        json=new_user_data,
        follow_redirects=True,
    )
    response_dict = response.json
    assert str(user_client_first.id) == response_dict['id']


def test__users_view__update_fail_client(client, user_client_second, first_client_auth_headers):
    new_user_data = {
        'first_name': 'first_name_test_client',
        'last_name': user_client_second.last_name,
        'middle_name': user_client_second.middle_name,
        'phone': user_client_second.phone,
        'email': user_client_second.email,
        'password': user_client_second.password,
    }
    response = client.put(
        f'/users/{user_client_second.id}',
        headers=first_client_auth_headers,
        json=new_user_data,
        follow_redirects=True,
    )

    assert response.status_code == 403


def test__users_view__update_fail_no_user(client, not_existing_uuid, admin_auth_headers):
    new_user_data = {
        'first_name': 'no_user',
        'last_name': 'no_user',
        'middle_name': 'no_user',
        'phone': 'no_user',
        'email': 'no_user',
        'password': 'no_user',
    }
    response = client.put(
        f'/users/{not_existing_uuid}',
        headers=admin_auth_headers,
        json=new_user_data,
        follow_redirects=True,
    )

    assert response.status_code == 404


def test__users_view__update_fail_no_field(client, user_client_second, admin_auth_headers):
    response = client.put(
        f'/users/{user_client_second.id}',
        headers=admin_auth_headers,
        follow_redirects=True,
    )

    assert response.status_code == 422


def test__users_view__delete_success(client, user_client_second, admin_auth_headers):
    response = client.delete(
        f'/users/{user_client_second.id}',
        follow_redirects=True,
        headers=admin_auth_headers,
    )
    response_dict = response.json
    user_in_db = get_by_id(Entities.USER, user_client_second.id)

    assert response_dict == {}
    assert user_in_db.is_deleted is True


def test__users_view__delete_fail_client_role(client, user_client_first, first_client_auth_headers):
    response = client.delete(
        f'/users/{user_client_first.id}',
        follow_redirects=True,
        headers=first_client_auth_headers,
    )

    assert response.status_code == 403


def test__users_view__delete_fail_no_user(client, not_existing_uuid, admin_auth_headers):
    response = client.delete(
        f'/users/{not_existing_uuid}',
        follow_redirects=True,
        headers=admin_auth_headers,
    )

    assert response.status_code == 404


def test__users_view__register_success(client, user_admin):
    user_data = {
        'first_name': 'test_register',
        'last_name': 'test_register',
        'middle_name': 'test_register',
        'phone': 'test_register',
        'email': 'test_register@test_register.ru',
        'password': 'test_register',
        'tg_id': '52525225255',
        'tg_username': 'test_register',
        'inviter_id': user_admin.id,
    }
    response = client.post(
        '/users/register',
        json=user_data,
        follow_redirects=True,
    )
    response_dict = response.json

    assert response_dict['access_token'] is not None

    user = get_list(Entities.USER, UsersGetListFilter(email=user_data['email']))['result'][0]
    delete(user.basket)
    delete(user)


def test__user_register_view___fail_no_required_field(client):
    user_data = {
        'first_name': 'second',
        'last_name': 'second',
        'middle_name': 'second',
        'phone': '79998887703',
    }
    response = client.post('/users/register', json=user_data, follow_redirects=True)
    assert response.status_code == 422


def test__user_register_view__fail_duplicate_uniq_field(client, user_admin):
    user_data = {
        'first_name': 'second',
        'last_name': 'second',
        'middle_name': 'second',
        'password': 'second',
        'phone': user_admin.phone,
    }
    response = client.post('/users/register', json=user_data, follow_redirects=True)
    assert response.status_code == 400


def test__user_login_view__success(client, user_admin, not_hash_admin_password):
    user_data = {
        'email': user_admin.email,
        'password': not_hash_admin_password,
    }
    response = client.post(
        '/users/login',
        json=user_data,
        follow_redirects=True,
    )
    response_dict = response.json
    assert response_dict['access_token'] is not None


def test__user_login_view__fail_no_required_field(client):
    user_data = {
        'email': 'second',
    }
    response = client.post('/users/login', json=user_data, follow_redirects=True)
    assert response.status_code == 422


def test__user_login_view__fail_pass_or_login_wrong(client):
    user_data = {
        'email': 'second',
        'password': 'second',
    }
    response = client.post('/users/login', json=user_data, follow_redirects=True)
    assert response.status_code == 400


def test__user_logout_view__success(client, admin_auth_headers):
    response = client.delete(
        '/users/logout',
        headers=admin_auth_headers,
        follow_redirects=True,
    )
    assert response.status_code == 200


def test__user_logout_view__fail_no_auth(client):
    response = client.delete(
        '/users/logout',
        follow_redirects=True,
    )
    assert response.status_code == 401


def test__user_logout_view__fail_token(client, not_existing_uuid):
    response = client.delete(
        '/users/logout',
        headers={'Authorization': f'Bearer {not_existing_uuid}'},
        follow_redirects=True,
    )
    assert response.status_code == 422
