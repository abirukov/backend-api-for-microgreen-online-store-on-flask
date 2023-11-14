import pytest

from beaver_app.blueprints.schemas import BaseGetListFilter
from beaver_app.blueprints.user.schemas import UsersGetListFilter
from beaver_app.db.db_utils import save, get_by_id, update, update_fields_by_id, get_list, \
    safe_delete, delete, get_search_params, get_query_params, query_process, is_entity_exist_by_field, \
    check_entity_by_unique_fields
from beaver_app.db.enums import SqlAlchemyFiltersOperands
from beaver_app.enums import Entities


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category')),
        (Entities.PRODUCT, pytest.lazy_fixture('product')),
        (Entities.USER, pytest.lazy_fixture('user_admin')),
        (Entities.BASKET, pytest.lazy_fixture('basket')),
    ],
)
def test__save(entity_type, model):
    save(model)

    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db

    delete(model_in_db)


@pytest.mark.parametrize(
    'entity_type, model, new_data',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category'), {'title': 'updated_title'}),
        (Entities.PRODUCT, pytest.lazy_fixture('product'), {'title': 'updated_title'}),
        (Entities.USER, pytest.lazy_fixture('user_admin'), {'first_name': 'updated_first_name'}),
        (Entities.BASKET, pytest.lazy_fixture('basket'), {'is_deleted': True}),
    ],
)
def test__update_fields_by_id(entity_type, model, new_data):
    update_fields_by_id(entity_type, model.id, new_data)

    model_in_db = get_by_id(entity_type, model.id)
    for field in new_data:
        assert getattr(model_in_db, field) == new_data[field]


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category')),
        (Entities.PRODUCT, pytest.lazy_fixture('product')),
        (Entities.USER, pytest.lazy_fixture('user_admin')),
        (Entities.BASKET, pytest.lazy_fixture('basket')),
    ],
)
def test__get_by_id(entity_type, model):
    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, model_id',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('not_existing_uuid')),
        (Entities.PRODUCT, pytest.lazy_fixture('not_existing_uuid')),
        (Entities.USER, pytest.lazy_fixture('not_existing_uuid')),
        (Entities.BASKET, pytest.lazy_fixture('not_existing_uuid')),
    ],
)
def test__get_by_id__not_existing_uuid(entity_type, model_id):
    model_in_db = get_by_id(entity_type, model_id)

    assert model_in_db is None


@pytest.mark.parametrize(
    'entity_type, models_list',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category_list')),
        (Entities.PRODUCT, pytest.lazy_fixture('product_list')),
        (Entities.USER, pytest.lazy_fixture('user_list')),
        (Entities.BASKET, pytest.lazy_fixture('basket_list')),
    ],
)
def test__get_list(entity_type, models_list):
    list_from_db = get_list(entity_type)['result']
    models_ids = [elem.id for elem in models_list]
    for elem in list_from_db:
        assert elem.id in models_ids


def test__get_list__search(user_admin):
    list_from_db = get_list(Entities.USER, UsersGetListFilter(search='admin'))['result']
    assert [user_admin] == list_from_db


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category')),
        (Entities.PRODUCT, pytest.lazy_fixture('product')),
        (Entities.USER, pytest.lazy_fixture('user_client_first')),
        (Entities.BASKET, pytest.lazy_fixture('basket')),
    ],
)
def test__safe_delete(entity_type, model):
    safe_delete(entity_type, model.id)

    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, model, new_data',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category'), {'title': 'updated_title'}),
        (Entities.PRODUCT, pytest.lazy_fixture('product'), {'title': 'updated_title'}),
        (Entities.USER, pytest.lazy_fixture('user_admin'), {'first_name': 'updated_first_name'}),
        (Entities.BASKET, pytest.lazy_fixture('basket'), {'is_deleted': True}),
    ],
)
def test__update(entity_type, model, new_data):
    for field in new_data:
        setattr(model, field, new_data[field])
    update(model)

    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category_for_delete')),
        (Entities.PRODUCT, pytest.lazy_fixture('product_for_delete')),
        (Entities.USER, pytest.lazy_fixture('user_client_for_delete')),
        (Entities.BASKET, pytest.lazy_fixture('basket_for_delete')),
    ],
)
def test__delete(entity_type, model) -> None:
    saved_model = save(model)
    delete(saved_model)

    model_in_db = get_by_id(entity_type, saved_model.id)

    assert model_in_db is None


@pytest.mark.parametrize(
    'fields_list, expected',
    [
        (
            [
                'first_name',
                'last_name',
                'middle_name',
                'phone',
                'email',
                'tg_id',
                'tg_username',
                'personal_code',
            ],
            {
                'or': [
                    {'field': 'first_name', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'last_name', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'middle_name', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'phone', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'email', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'tg_id', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'tg_username', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'personal_code', 'op': 'ilike', 'value': '%test%'},
                ],
            },
        ),
        (
            ['title'],
            {'or': [{'field': 'title', 'op': 'ilike', 'value': '%test%'}]},
        ),
        (
            ['title', 'description'],
            {
                'or': [
                    {'field': 'title', 'op': 'ilike', 'value': '%test%'},
                    {'field': 'description', 'op': 'ilike', 'value': '%test%'},
                ],
            },
        ),
    ],
)
def test__get_search_params(fields_list, expected):
    assert get_search_params('test', fields_list) == expected


@pytest.mark.parametrize(
    'params_list, expected',
    [
        (
            None,
            {
                'filter_params': [{'and': []}],
                'sort_params': None,
                'page_number': 1,
                'page_size': 20,
            },
        ),
        (
            BaseGetListFilter(page_number=2, page_size=10),
            {
                'filter_params': [{'and': []}],
                'sort_params': None,
                'page_number': 2,
                'page_size': 10,
            },
        ),
        (
            BaseGetListFilter(
                is_deleted=True,
                created_at_before='2023-06-05T15:00:00',
                created_at_after='2023-02-05T15:00:00',
                search='test',
            ),
            {
                'filter_params': [{'and': [
                    {
                        'field': 'is_deleted',
                        'op': SqlAlchemyFiltersOperands.EQUAL.value,
                        'value': True,
                    },
                    {
                        'field': 'created_at',
                        'op': SqlAlchemyFiltersOperands.LESS_OR_EQUAL.value,
                        'value': '2023-06-05T15:00:00',
                    },
                    {
                        'field': 'created_at',
                        'op': SqlAlchemyFiltersOperands.MORE_OR_EQUAL.value,
                        'value': '2023-02-05T15:00:00',
                    },
                ]}],
                'sort_params': None,
                'page_number': 1,
                'page_size': 20,
            },
        ),
        (
            BaseGetListFilter(sort_by_created_at='asc'),
            {
                'filter_params': [{'and': []}],
                'sort_params': [{
                    'field': 'created_at',
                    'direction': 'asc',
                }],
                'page_number': 1,
                'page_size': 20,
            },
        ),
    ],
)
def test__get_query_params(params_list, expected):
    assert get_query_params(params_list) == expected


def test__query_process(product):
    query = Entities.PRODUCT.value.query
    query_params = {
        'filter_params': [{'and': [{
            'or': [
                {
                    'field': 'title',
                    'op': SqlAlchemyFiltersOperands.ILIKE.value,
                    'value': '%тест%',
                },
                {
                    'field': 'description',
                    'op': SqlAlchemyFiltersOperands.ILIKE.value,
                    'value': '%тест%',
                },
            ],
        }]}],
        'sort_params': [{
            'field': 'created_at',
            'direction': 'asc',
        }],
        'page_number': 1,
        'page_size': 20,
    }

    assert query_process(query, query_params)['result'] == [product]


@pytest.mark.parametrize(
    'entity_type, model, field, value, expected',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category'), 'title', 'Категория тест', True),
        (Entities.CATEGORY, pytest.lazy_fixture('category'), 'title', 'тест', False),
        (Entities.PRODUCT, pytest.lazy_fixture('product'), 'title', 'Товар тест', True),
        (Entities.PRODUCT, pytest.lazy_fixture('product'), 'title', 'тест', False),
        (Entities.USER, pytest.lazy_fixture('user_admin'), 'tg_id', '555555555', True),
        (Entities.USER, pytest.lazy_fixture('user_admin'), 'tg_id', '555555556', False),
    ],
)
def test_is_entity_exist_by_field(entity_type, model, field, value, expected):  # noqa: U100
    assert is_entity_exist_by_field(entity_type, field, value) == expected


@pytest.mark.parametrize(
    'entity_type, model, unique_attrs, data, expected',
    [
        (
            Entities.CATEGORY,
            pytest.lazy_fixture('category'),
            ['title'],
            Entities.CATEGORY.value(title='Категория тест'),
            ['title'],
        ),
        (
            Entities.CATEGORY,
            pytest.lazy_fixture('category'),
            ['title'],
            Entities.CATEGORY.value(title='тест'),
            [],
        ),
        (
            Entities.PRODUCT,
            pytest.lazy_fixture('product'),
            ['title', 'price'],
            Entities.PRODUCT.value(title='Товар тест', price=130.0),
            ['title'],
        ),
        (
            Entities.PRODUCT,
            pytest.lazy_fixture('product'),
            ['title', 'price'],
            Entities.PRODUCT.value(title='тест', price=130.0),
            [],
        ),
        (
            Entities.USER,
            pytest.lazy_fixture('user_admin'),
            ['phone', 'email', 'tg_id'],
            pytest.lazy_fixture('user_admin_unsaved'),
            ['phone', 'email', 'tg_id'],
        ),
        (
            Entities.USER,
            pytest.lazy_fixture('user_admin'),
            ['phone', 'email', 'tg_id'],
            pytest.lazy_fixture('user_client_first_unsaved'),
            [],
        ),
    ],
)
def test_check_entity_by_unique_fields(entity_type, model, unique_attrs, data, expected):  # noqa: U100
    assert check_entity_by_unique_fields(entity_type, unique_attrs, data) == expected
