import uuid

import sqlalchemy
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters

from beaver_app.db.db import db_session, Base
from beaver_app.enums import Entities
from beaver_app.db.enums import SqlAlchemyFiltersOperands


def save(db_model: Base) -> Base:
    db_session.add(db_model)
    db_session.commit()
    return db_model


def update_fields_by_id(entity_type: Entities, id: int | uuid.UUID, new_fields: dict) -> None:
    db_session.query(entity_type.value).filter(
        entity_type.value.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    db_session.commit()


def get_by_id(entity_type: Entities, id: int | uuid.UUID) -> Base | None:
    return entity_type.value.query.filter(entity_type.value.id == id).first()


def get_list(entity_type: Entities, q_filter=None) -> dict:
    query = entity_type.value.query
    query_params = get_query_params(q_filter)
    if q_filter is not None and 'search' in q_filter:
        search_fields = entity_type.value.get_search_fields()
        additional_search_params = get_search_params(q_filter['search'], search_fields)
        query_params['filter_params'][0]['and'].append(additional_search_params)
    return query_process(query, query_params)


def safe_delete(entity_type: Entities, id: int | uuid.UUID) -> None:
    update_fields_by_id(entity_type, id, {'is_deleted': True})


def update(model_obj):
    assert model_obj.id
    db_session.add(model_obj)
    db_session.commit()
    return model_obj


def delete(model_obj) -> None:
    db_session.delete(model_obj)
    db_session.commit()


def get_query_params(q_filter: dict | None) -> dict:
    query_params: dict = {
        'filter_params': [{'and': []}],
        'sort_params': None,
        'page_number': 1,
        'page_size': 20,
    }
    if q_filter is None:
        return query_params

    for param_name in q_filter:
        if param_name.endswith('_before') or param_name.endswith('_less'):
            query_params['filter_params'][0]['and'].append(
                {
                    'field': param_name.replace('_before', '').replace('_less', ''),
                    'op': SqlAlchemyFiltersOperands.LESS_OR_EQUAL.value,
                    'value': q_filter[param_name],
                },
            )
        elif param_name.endswith('_after') or param_name.endswith('_more'):
            query_params['filter_params'][0]['and'].append(
                {
                    'field': param_name.replace('_after', '').replace('_more', ''),
                    'op': SqlAlchemyFiltersOperands.MORE_OR_EQUAL.value,
                    'value': q_filter[param_name],
                },
            )
        elif param_name.startswith('sort_by_'):
            query_params['sort_params'] = [{
                'field': param_name.replace('sort_by_', ''),
                'direction': q_filter[param_name],
            }]
        elif param_name == 'page_number' or param_name == 'page_size':
            query_params[param_name] = q_filter[param_name]
        elif param_name == 'search':
            continue
        else:
            query_params['filter_params'][0]['and'].append(
                {
                    'field': param_name,
                    'op': SqlAlchemyFiltersOperands.EQUAL.value,
                    'value': q_filter[param_name],
                },
            )
    return query_params


def get_search_params(search_value: str, fields: list) -> dict:
    list_result: dict = {'or': []}
    for field in fields:
        list_result['or'].append({
            'field': field,
            'op': SqlAlchemyFiltersOperands.ILIKE.value,
            'value': f'%{search_value}%',
        })
    return list_result


def query_process(query: sqlalchemy.orm.query.Query, query_params: dict):
    if query_params['filter_params'][0]['and']:
        query = apply_filters(query, query_params['filter_params'])
    if query_params['sort_params'] is not None:
        query = apply_sort(query, query_params['sort_params'])

    query, pagination = apply_pagination(
        query,
        page_number=query_params['page_number'],
        page_size=query_params['page_size'],
    )
    return {
        'result': query.all(),
        'pagination': pagination,
    }
