import json

from beaver_app.db.db_utils import get_by_id, delete
from beaver_app.enums import Entities


def test__categories_view__list(client, category_list):
    response = client.get("/categories", follow_redirects=True)
    count_entries = 0
    for category in category_list:
        if f'"id":"{str(category.id)}"' in response.data.decode():
            count_entries += 1

    assert count_entries == len(category_list)


def test__categories_view__create_success(client):
    category_data = {"title": "Категория успешный тест"}
    response = client.post("/categories", json=category_data, follow_redirects=True)
    response_dict = json.loads(response.data.decode())

    assert category_data["title"] == response_dict["title"]

    category = get_by_id(Entities.CATEGORY, response_dict["id"])
    delete(category)


def test__categories_view__create_fail_not_existing_field(client):
    category_data = {
        "some_field": "some_value",
        "title": "title",
    }
    response = client.post("/categories", json=category_data, follow_redirects=True)

    assert response.status_code == 422


def test__categories_view__create_fail_empty(client):
    category_data = {}
    response = client.post("/categories", json=category_data, follow_redirects=True)

    assert response.status_code == 422


def test__categories_view__get_success(client, saved_category):
    response = client.get(f"/categories/{saved_category.id}", follow_redirects=True)
    response_dict = json.loads(response.data.decode())

    assert str(saved_category.id) == response_dict["id"]


def test__categories_view__get_fail(client, not_existing_uuid):
    response = client.get(f"/categories/{not_existing_uuid}", follow_redirects=True)

    assert response.status_code == 404


def test__categories_view__update_success(client, saved_category):
    new_category_data = {"title": "title"}
    response = client.put(f"/categories/{saved_category.id}", json=new_category_data, follow_redirects=True)
    response_dict = json.loads(response.data.decode())

    assert response_dict["title"] == "title"


def test__categories_view__update_fail(client, not_existing_uuid):
    new_category_data = {"title": "title"}
    response = client.put(f"/categories/{not_existing_uuid}", json=new_category_data, follow_redirects=True)

    assert response.status_code == 404


def test__categories_view__delete_success(client, saved_category):
    response = client.delete(f"/categories/{saved_category.id}", follow_redirects=True)
    response_dict = json.loads(response.data.decode())
    category_in_db = get_by_id(Entities.CATEGORY, saved_category.id)

    assert response_dict == {}
    assert category_in_db.is_deleted is True


def test__categories_view__delete_fail(client, not_existing_uuid):
    response = client.delete(f"/categories/{not_existing_uuid}", follow_redirects=True)

    assert response.status_code == 404
