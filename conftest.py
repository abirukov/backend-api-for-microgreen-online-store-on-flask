import pytest
from beaver_app.app import create_app
from beaver_app.blueprints.category.models import Category
from beaver_app.blueprints.product.models import Product
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
        title='Товар тест удаление',
        price=120.0,
        description='Описание товара тест',
        category_id=saved_category.id,
    )


@pytest.fixture()
def saved_product(product):
    save(product)
    yield product
    Product.query.filter_by(id=product.id).delete()
    db_session.commit()


@pytest.fixture()
def saved_product_for_delete(product_for_delete):
    save(product_for_delete)
    yield product_for_delete
    Product.query.filter_by(id=product_for_delete.id).delete()
    db_session.commit()


@pytest.fixture()
def category_list(saved_category, saved_category_for_delete):
    return [saved_category, saved_category_for_delete]


@pytest.fixture()
def product_list(saved_product, saved_product_for_delete):
    return [saved_product, saved_product_for_delete]
