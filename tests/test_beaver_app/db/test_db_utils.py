import pytest

from beaver_app.db.db_utils import save, get_by_id, update, update_fields_by_id, get_list, safe_delete, create, delete
from beaver_app.enums import Entities


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('saved_category')),
        (Entities.PRODUCT, pytest.lazy_fixture('saved_product')),
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
        (Entities.CATEGORY, pytest.lazy_fixture('saved_category'), {'title': 'updated_title'}),
        (Entities.PRODUCT, pytest.lazy_fixture('saved_product'), {'title': 'updated_title'}),
    ],
)
def test__update_fields_by_id(entity_type, model, new_data):
    update_fields_by_id(entity_type, model.id, new_data)

    model_in_db = get_by_id(entity_type, model.id)
    for field in new_data:
        setattr(model, field, new_data[field])

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('saved_category')),
        (Entities.PRODUCT, pytest.lazy_fixture('saved_product')),
    ],
)
def test__get_by_id(entity_type, model):
    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, models_list',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category_list')),
        (Entities.PRODUCT, pytest.lazy_fixture('product_list')),
    ],
)
def test__get_list(entity_type, models_list):
    list_from_db = get_list(entity_type)['result']

    assert models_list == list_from_db


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('saved_category')),
        (Entities.PRODUCT, pytest.lazy_fixture('saved_product')),
    ],
)
def test__safe_delete(entity_type, model):
    safe_delete(entity_type, model.id)

    model_in_db = get_by_id(entity_type, model.id)

    assert model == model_in_db


@pytest.mark.parametrize(
    'entity_type, model, new_data',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('saved_category'), {'title': 'updated_title'}),
        (Entities.PRODUCT, pytest.lazy_fixture('saved_product'), {'title': 'updated_title'}),
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
        (Entities.CATEGORY, pytest.lazy_fixture('category')),
        (Entities.PRODUCT, pytest.lazy_fixture('product')),
    ],
)
def test__create(entity_type, model):
    saved_model = create(model)

    model_in_db = get_by_id(entity_type, saved_model.id)

    assert saved_model == model_in_db

    delete(saved_model)


@pytest.mark.parametrize(
    'entity_type, model',
    [
        (Entities.CATEGORY, pytest.lazy_fixture('category')),
        (Entities.PRODUCT, pytest.lazy_fixture('product')),
    ],
)
def test__delete(entity_type, model) -> None:
    saved_model = create(model)
    id = saved_model.id
    delete(saved_model)

    model_in_db = get_by_id(entity_type, id)

    assert model_in_db is None
