import pytest
from werkzeug.security import generate_password_hash

from beaver_app.app import create_app
from beaver_app.blueprints.basket.models import Basket, BasketProduct
from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.product.models import Product
from beaver_app.blueprints.user.models import User
from beaver_app.db.db import db_session
from beaver_app.db.db_utils import save


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SERVER_NAME': 'localhost',
    })
    with (
        app.app_context(),
        app.test_request_context(),
        app.test_client(),
    ):
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def config():
    return {
        'POSTGRES_DBNAME': 'postgres',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'devpass',
    }


@pytest.fixture
def not_existing_uuid():
    return 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'


@pytest.fixture()
def category_unsaved():
    return Category(title='Категория тест')


@pytest.fixture()
def category_for_delete_unsaved():
    return Category(title='Категория тест удаление')


@pytest.fixture()
def category(category_unsaved):
    save(category_unsaved)
    yield category_unsaved
    Product.query.filter_by(category_id=category_unsaved.id).delete()
    Category.query.filter_by(id=category_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def category_for_delete(category_for_delete_unsaved):
    save(category_for_delete_unsaved)
    yield category_for_delete_unsaved
    Category.query.filter_by(id=category_for_delete_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def product_unsaved(category):
    return Product(
        title='Товар тест',
        price=120.0,
        description='Описание товара тест',
        category_id=category.id,
    )


@pytest.fixture()
def product_for_delete_unsaved(category):
    return Product(
        title='Товар удаление',
        price=120.0,
        description='Описание товар удаление',
        category_id=category.id,
    )


@pytest.fixture()
def product(product_unsaved):
    save(product_unsaved)
    yield product_unsaved
    BasketProduct.query.filter_by(product_id=product_unsaved.id).delete()
    Product.query.filter_by(id=product_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def product_for_delete(product_for_delete_unsaved):
    save(product_for_delete_unsaved)
    yield product_for_delete_unsaved


@pytest.fixture()
def category_list(category, category_for_delete):
    return [category, category_for_delete]


@pytest.fixture()
def product_list(product, product_for_delete):
    return [product, product_for_delete]


@pytest.fixture()
def not_hash_admin_password():
    return 'admin@admin.ru'


@pytest.fixture()
def user_admin_unsaved(not_hash_admin_password):
    return User(
        first_name='admin',
        last_name='admin',
        middle_name='admin',
        phone='79998887766',
        email='admin@admin.ru',
        password=not_hash_admin_password,
        tg_id='555555555',
        tg_username='adminadmin',
        personal_code='AD11',
        is_admin=True,
        inviter_id=None,
    )


@pytest.fixture()
def user_client_first_unsaved(user_admin):
    return User(
        first_name='first',
        last_name='first',
        middle_name='first',
        phone='79998887701',
        email='first@first.ru',
        password='first@first.ru',
        tg_id='1111111111',
        tg_username='firstfirst',
        personal_code='FT11',
        inviter_id=user_admin.id,
    )


@pytest.fixture()
def user_client_for_delete_unsaved(user_admin):
    return User(
        first_name='for_delete',
        last_name='for_delete',
        middle_name='for_delete',
        phone='79998887702',
        email='for_delete@for_delete.ru',
        password='for_delete@for_delete.ru',
        tg_id='3111111111',
        tg_username='for_deletefor_delete',
        personal_code='FD11',
        inviter_id=user_admin.id,
    )


@pytest.fixture()
def user_client_second_unsaved(user_admin):
    return User(
        first_name='second',
        last_name='second',
        middle_name='second',
        phone='79998887703',
        email='second@second.ru',
        password='second@second.ru',
        tg_id='2111111111',
        tg_username='secondsecond',
        personal_code='FS11',
        inviter_id=user_admin.id,
    )


@pytest.fixture()
def user_admin(user_admin_unsaved):
    user_admin_unsaved.password = generate_password_hash(user_admin_unsaved.password)
    save(user_admin_unsaved)
    yield user_admin_unsaved
    User.query.filter_by(id=user_admin_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def user_client_first(user_client_first_unsaved):
    user_client_first_unsaved.password = generate_password_hash(user_client_first_unsaved.password)
    save(user_client_first_unsaved)
    yield user_client_first_unsaved
    User.query.filter_by(id=user_client_first_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def user_client_second(user_client_for_delete_unsaved):
    user_client_for_delete_unsaved.password = generate_password_hash(user_client_for_delete_unsaved.password)
    save(user_client_for_delete_unsaved)
    yield user_client_for_delete_unsaved
    User.query.filter_by(id=user_client_for_delete_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def user_client_for_delete(user_client_for_delete_unsaved):
    user_client_for_delete_unsaved.password = generate_password_hash(user_client_for_delete_unsaved.password)
    save(user_client_for_delete_unsaved)
    yield user_client_for_delete_unsaved
    User.query.filter_by(id=user_client_for_delete_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def user_list(
    user_admin,
    user_client_first,
    user_client_second,
    user_client_for_delete,
):
    return [
        user_admin,
        user_client_first,
        user_client_second,
        user_client_for_delete,
    ]


@pytest.fixture()
def admin_auth_headers(user_admin):
    return {'Authorization': f'Bearer {user_admin.create_token()}'}


@pytest.fixture()
def first_client_auth_headers(user_client_first):
    return {'Authorization': f'Bearer {user_client_first.create_token()}'}


@pytest.fixture()
def basket_unsaved(user_client_first):
    return Basket(user_id=user_client_first.id)


@pytest.fixture()
def basket_for_delete_unsaved(user_client_first):
    return Basket(user_id=user_client_first.id)


@pytest.fixture()
def basket(basket_unsaved):
    save(basket_unsaved)
    yield basket_unsaved
    BasketProduct.query.filter_by(basket_id=basket_unsaved.id).delete()
    Basket.query.filter_by(id=basket_unsaved.id).delete()
    db_session.commit()


@pytest.fixture()
def basket_for_delete(basket_for_delete_unsaved):
    save(basket_for_delete_unsaved)
    yield basket_for_delete_unsaved


@pytest.fixture()
def basket_product_unsaved(basket, product):
    return BasketProduct(
        basket_id=basket.id,
        product_id=product.id,
        quantity=3,
    )


@pytest.fixture()
def basket_product(basket_product_unsaved):
    save(basket_product_unsaved)
    yield basket_product_unsaved
    BasketProduct.query.filter_by(
        basket_id=basket_product_unsaved.basket_id,
        product_id=basket_product_unsaved.basket_id,
    ).delete()
    db_session.commit()


@pytest.fixture()
def basket_list(basket):
    return [basket]
