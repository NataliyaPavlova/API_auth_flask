from flask_restx import Resource
from flask_restx._http import HTTPStatus
from src.error_handlers import InvalidAPIUsage
from src.messages.api_error import APIError
from src.models.responces import user_response, user_role_response
from src.service.decorators import admin_required
from src.service.user import get_user_service
from src.views.v1.api import api, get_resource_url, ResourceName

user_ns = api.namespace(
    'users',
    description='Operations with users.',
    path=get_resource_url(ResourceName.USER),
)

service = get_user_service()


@user_ns.route('/')
class userList(Resource):
    """Shows a list of all users, and lets you POST to add new users"""

    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_response)
    @admin_required()
    def get(self):
        """List all users"""
        users = service.filter_by()
        return users


@user_ns.route('/<string:id>')
class userUD(Resource):
    """Show a single user item and lets you delete them"""

    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_response)
    @admin_required()
    def get(self, id):
        """Fetch a given resource"""
        if user := service.get(id):
            return user
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)

    @user_ns.doc('update_user_role')
    @user_ns.expect(user_role_response)
    @user_ns.marshal_with(user_response)
    @admin_required()
    def put(self, id: str):
        """Update a user given its identifier"""
        if user := service.update(id, **api.payload):
            return user, HTTPStatus.OK
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)
