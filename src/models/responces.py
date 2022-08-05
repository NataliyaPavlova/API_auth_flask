from flask_restx import fields

from src.views.v1.api import api

permission_response = api.model('Permission', {
    'id': fields.String(
        readonly=True,
        description='The permission unique identifier'
    ),
    'title': fields.String(
        required=True,
        description='The permission title'
    ),
    'created': fields.DateTime(
        required=False,
        description='Date and time of permission creation',
    ),
    'modified': fields.DateTime(
        require=False,
        description='Date and time of permission last modification'
    ),
})

permission_id_response = api.model('permission_id', {
    'permission_id': fields.String(
        required=True,
        description='The permission unique identifier'
    ),
})

role_response = api.model('Role', {
    'id': fields.String(
        readonly=True,
        description='The role unique identifier'
    ),
    'title': fields.String(
        required=True,
        description='The role title'
    ),
    'created': fields.DateTime(
        required=False,
        description='Date and time of role creation',
    ),
    'modified': fields.DateTime(
        require=False,
        description='Date and time of last modification of role'
    ),
})

user_response = api.model('user', {
    'id': fields.String(
        readonly=True,
        description='The user unique identifier'
    ),
    'login': fields.String(
        required=True,
        description='The user title'
    ),
    'password': fields.String(
        required=False,
        description='The user password'
    ),
    'created': fields.DateTime(
        required=False,
        description='Date and time of user creation',
    ),
    'modified': fields.DateTime(
        require=False,
        description='Date and time of last modification of user'
    ),
    'role_title': fields.String(
        required=False,
        description='Role of user'
    ),
})

user_role_response = api.model('user_role', {
    'role_id': fields.String(
        required=True,
        description='Role of user'
    ),
})
