from flask_restx import fields

from src.views.v1.api import api

profile_change_request = api.model('profile_change_request', {
    'new_pwd': fields.String(
        required=True,
        description='New password'
    ),
    'login': fields.String(
        required=True,
        description='Old Login'
    ),
    'new_login': fields.String(
        required=True,
        description='New Login'
    ),
})

only_login_request = api.model('only_login', {
    'login': fields.String(
        required=True,
        description='Old Login'
    ),
})
