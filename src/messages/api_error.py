from enum import Enum

from flask_restx._http import HTTPStatus


class APIError(str, Enum):
    NOT_FOUND = 'Item not found'
    ALREADY_EXIST = 'Item already exist'
    MISSING_PARAMETER = 'Missing required parameter'


def get_error_response(http_status: HTTPStatus, description: APIError) -> dict:
    return {
        'code': http_status.value,
        'message': description.value,
    }
