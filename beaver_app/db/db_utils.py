from beaver_app.blueprints.product.models.product import Product
from beaver_app.blueprints.category.models.category import Category
from beaver_app.db.db import db_session
from beaver_app.enums import Entities


def save(db_model: Product | Category) -> Product | Category:
    db_session.add(db_model)
    db_session.commit()
    return db_model


def update_fields_by_id(type: Entities, id: int, new_fields: dict) -> None:
    db_session.query(type.value).filter(
        type.value.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    db_session.commit()


def get_by_id(type: Entities, id: int) -> Product | Category | None:
    return type.value.query.filter(type.value.id == id).first()


def get_list(type: Entities) -> list[Product | Category | None]:
    print(type.value)
    return type.value.query.all()


def safe_delete(type: Entities, id: int) -> None:
    update_fields_by_id(type, id, {'is_deleted': True})


def update(model_obj):
    assert model_obj.id
    db_session.add(model_obj)
    db_session.commit()
    return model_obj


def create(model_obj):
    db_session.add(model_obj)
    db_session.commit()
    return model_obj


def delete(model_obj) -> None:
    db_session.delete(model_obj)
    db_session.commit()
