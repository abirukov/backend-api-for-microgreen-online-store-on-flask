from beaver_app.blueprints.utils import response_unique_fields_error


def test_response_unique_fields_error(app):  # noqa: U100
    response = response_unique_fields_error(['test_field1', 'test_field2'])
    assert response.status_code == 400
    assert response.data == b'{"error":["test_field1 already exists","test_field2 already exists"]}\n'
