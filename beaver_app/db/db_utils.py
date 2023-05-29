import uuid

from beaver_app.db.db import db_session, Base
from beaver_app.enums import Entities


def save(db_model: Base) -> Base:
    db_session.add(db_model)
    db_session.commit()
    return db_model


def update_fields_by_id(type: Entities, id: int | uuid.UUID, new_fields: dict) -> None:
    db_session.query(type.value).filter(
        type.value.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    db_session.commit()


def get_by_id(type: Entities, id: int | uuid.UUID) -> Base | None:
    return type.value.query.filter(type.value.id == id).first()


def get_list(type: Entities) -> list[Base | None]:
    return type.value.query.all()


def safe_delete(type: Entities, id: int | uuid.UUID) -> None:
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
