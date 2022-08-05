from enum import Enum

from flask_restx import Api

api = Api()

api.version = '1.0'
api.title = 'Authorization API'
api.description = 'Authorization API for online cinema.'

API_PREFIX = f'/api/v{api.version}'


class ResourceName(str, Enum):
    PERMISSION = '/permissions'
    ROLE = '/roles'
    USER = '/users'
    PROFILE = '/profile'
    AUTH = '/auth'


def get_resource_url(resource: ResourceName) -> str:
    return f'{API_PREFIX}{resource.value}'
