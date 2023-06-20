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
def category():
    return Category(title='Категория тест')


@pytest.fixture()
def category_for_delete():
    return Category(title='Категория тест удаление')


@pytest.fixture()
def saved_category(category):
    save(category)
    yield category
    Product.query.filter_by(category_id=category.id).delete()
    Category.query.filter_by(id=category.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_category_for_delete(category_for_delete):
    save(category_for_delete)
    yield category_for_delete
    Category.query.filter_by(id=category_for_delete.id).delete()
    db_session.commit()


@pytest.fixture()
def product(saved_category):
    return Product(
        title='Товар тест',
        price=120.0,
        description='Описание товара тест',
        category_id=saved_category.id,
    )


@pytest.fixture()
def product_for_delete(saved_category):
    return Product(
        title='Товар удаление',
        price=120.0,
        description='Описание товар удаление',
        category_id=saved_category.id,
    )


@pytest.fixture()
def saved_product(product):
    save(product)
    yield product
    BasketProduct.query.filter_by(product_id=product.id).delete()
    Product.query.filter_by(id=product.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_product_for_delete(product_for_delete):
    save(product_for_delete)
    yield product_for_delete


@pytest.fixture()
def category_list(saved_category, saved_category_for_delete):
    return [saved_category, saved_category_for_delete]


@pytest.fixture()
def product_list(saved_product, saved_product_for_delete):
    return [saved_product, saved_product_for_delete]


@pytest.fixture()
def not_hash_admin_password():
    return 'admin@admin.ru'


@pytest.fixture()
def user_admin(not_hash_admin_password):
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
def user_client_first(saved_user_admin):
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
        inviter_id=saved_user_admin.id,
    )


@pytest.fixture()
def user_client_for_delete(saved_user_admin):
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
        inviter_id=saved_user_admin.id,
    )


@pytest.fixture()
def user_client_second(saved_user_admin):
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
        inviter_id=saved_user_admin.id,
    )


@pytest.fixture()
def saved_user_admin(user_admin):
    user_admin.password = generate_password_hash(user_admin.password)
    save(user_admin)
    yield user_admin
    User.query.filter_by(id=user_admin.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_user_client_first(user_client_first):
    user_client_first.password = generate_password_hash(user_client_first.password)
    save(user_client_first)
    yield user_client_first
    User.query.filter_by(id=user_client_first.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_user_client_second(user_client_second):
    user_client_second.password = generate_password_hash(user_client_second.password)
    save(user_client_second)
    yield user_client_second
    User.query.filter_by(id=user_client_second.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_user_client_for_delete(user_client_for_delete):
    user_client_for_delete.password = generate_password_hash(user_client_for_delete.password)
    save(user_client_for_delete)
    yield user_client_for_delete
    User.query.filter_by(id=user_client_for_delete.id).delete()
    db_session.commit()


@pytest.fixture()
def user_list(
    saved_user_admin,
    saved_user_client_first,
    saved_user_client_second,
    saved_user_client_for_delete,
):
    return [
        saved_user_admin,
        saved_user_client_first,
        saved_user_client_second,
        saved_user_client_for_delete,
    ]


@pytest.fixture()
def admin_auth_headers(saved_user_admin):
    return {'Authorization': f'Bearer {saved_user_admin.create_token()}'}


@pytest.fixture()
def first_client_auth_headers(saved_user_client_first):
    return {'Authorization': f'Bearer {saved_user_client_first.create_token()}'}


@pytest.fixture()
def basket(saved_user_client_first):
    return Basket(user_id=saved_user_client_first.id)


@pytest.fixture()
def basket_for_delete(saved_user_client_first):
    return Basket(user_id=saved_user_client_first.id)


@pytest.fixture()
def saved_basket(basket):
    save(basket)
    yield basket
    BasketProduct.query.filter_by(basket_id=basket.id).delete()
    Basket.query.filter_by(id=basket.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_basket_for_delete(basket_for_delete):
    save(basket_for_delete)
    yield basket_for_delete


@pytest.fixture()
def basket_product(saved_basket, saved_product):
    return BasketProduct(
        basket_id=saved_basket.id,
        product_id=saved_product.id,
        quantity=3,
    )


@pytest.fixture()
def saved_basket_product(basket_product):
    save(basket_product)
    yield basket_product
    BasketProduct.query.filter_by(
        basket_id=basket_product.basket_id,
        product_id=basket_product.basket_id,
    ).delete()
    db_session.commit()


@pytest.fixture()
def basket_list(saved_basket):
    return [saved_basket]
