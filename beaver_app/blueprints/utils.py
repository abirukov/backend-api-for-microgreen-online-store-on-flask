from flask import Response, make_response, jsonify


def response_unique_fields_error(exist_attrs: list) -> Response:
    response_message: dict = {'error': []}
    for attr in exist_attrs:
        response_message['error'].append(f'{attr} already exists')
    return make_response(jsonify(response_message), 400)
