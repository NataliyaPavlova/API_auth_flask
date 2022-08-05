from flask import jsonify
from http import HTTPStatus


def make_success_response(result: dict):
    return jsonify({"response": "success", "result": result, 'status': HTTPStatus.OK})


def make_error_response(description: str, status: int = HTTPStatus.BAD_REQUEST):
    return jsonify({"response": "error", "description": description, 'status': status})
