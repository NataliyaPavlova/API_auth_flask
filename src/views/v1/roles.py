from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from src.error_handlers import InvalidAPIUsage
from src.messages.api_error import APIError
from src.models.responces import permission_id_response
from src.models.responces import role_response, permission_response
from src.service.decorators import admin_required
from src.service.role import get_role_service
from src.views.v1.api import api
from src.views.v1.api import get_resource_url, ResourceName

role_ns = api.namespace(
    'roles',
    description='Operations with roles.',
    path=get_resource_url(ResourceName.ROLE),
)

service = get_role_service()


@role_ns.route('/')
class RoleList(Resource):
    """
    Shows a list of all roles, and lets you POST to add new roles
    """

    @role_ns.doc('list_roles')
    @role_ns.marshal_list_with(role_response)
    @admin_required()
    def get(self):
        """List all roles"""
        roles = service.filter_by()
        return roles

    @role_ns.doc('create_role')
    @role_ns.marshal_with(role_response)
    @admin_required()
    def post(self):
        """Create a new roles"""
        if title := request.form.get('title', None):
            role = service.add(title=title)
            if role:
                return role, HTTPStatus.CREATED
            raise InvalidAPIUsage(APIError.ALREADY_EXIST,
                                  status_code=HTTPStatus.NOT_ACCEPTABLE)

        raise InvalidAPIUsage(APIError.MISSING_PARAMETER,
                              status_code=HTTPStatus.BAD_REQUEST)


@role_ns.route('/<string:id>')
class RoleUD(Resource):
    """Show a single role item and lets you delete them"""

    @role_ns.doc('get_role')
    @role_ns.marshal_with(role_response)
    @admin_required()
    def get(self, id):
        """Fetch a given resource"""
        if role := service.get(id):
            return role
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)

    @role_ns.doc('delete_role')
    @admin_required()
    def delete(self, id):
        """Delete a role given its identifier"""
        if service.delete(id):
            return {}, HTTPStatus.OK
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)

    @role_ns.doc('update_role')
    @role_ns.expect(role_response)
    @role_ns.marshal_with(role_response)
    @admin_required()
    def put(self, id):
        """Update a role given its identifier"""
        if role := service.update(api.payload):
            return role, HTTPStatus.OK
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)


@role_ns.route(f'/<string:id>{ResourceName.PERMISSION.value}')
class RolePermission(Resource):
    """Show a single role item and lets you delete them"""

    @role_ns.doc('get_role_permissions')
    @role_ns.marshal_list_with(permission_response)
    @admin_required()
    def get(self, id):
        """Fetch a given resource"""
        if permissions := service.get_permissions(id):
            return permissions
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)

    @role_ns.doc('add_role_permission')
    @role_ns.expect(permission_id_response)
    @role_ns.marshal_list_with(permission_response)
    @admin_required()
    def post(self, id):
        """Add a permission to role"""
        if role := service.add_permission(id, **api.payload):
            return role, HTTPStatus.OK
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)


@role_ns.route(f'/<string:id>{ResourceName.PERMISSION.value}/<string:id_perm>')
class RolePermissionCD(Resource):

    @role_ns.doc('delete_role_permission')
    @admin_required()
    def delete(self, id):
        """Delete a role given its identifier"""
        if service.delete(id):
            return {}, HTTPStatus.OK
        raise InvalidAPIUsage(APIError.NOT_FOUND,
                              status_code=HTTPStatus.NOT_FOUND)
