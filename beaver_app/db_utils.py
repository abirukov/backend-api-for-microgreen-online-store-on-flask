from flask import current_app
from sqlalchemy import select

from beaver_app.blueprints.product.models.product import Product
from beaver_app.blueprints.category.models.category import Category
from beaver_app.enums import Entities

session = current_app.session


def save(db_model: Product | Category) -> Product | Category:
    session.add(db_model)
    session.commit()
    return db_model


def update_fields_by_id(type: Entities, id: int, new_fields: dict) -> None:
    session.query(type.value).filter(
        type.value.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    session.commit()


def get_by_id(type: Entities, id: int) -> Product | Category | None:
    return type.value.query.filter(type.value.id == id).first()


def get_list(type: Entities) -> list[Product | Category | None]:
    return current_app.session.execute(select(type).fetchall())


def safe_delete(type: Entities, id: int) -> None:
    update_fields_by_id(type, id, {'is_deleted': True})


def update(model_obj):
    assert model_obj.id
    session.add(model_obj)
    session.commit()
    return model_obj


def create(model_obj):
    session.add(model_obj)
    session.commit()
    return model_obj


def delete(model_obj) -> None:
    session.delete(model_obj)
    session.commit()
