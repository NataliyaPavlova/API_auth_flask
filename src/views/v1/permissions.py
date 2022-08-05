from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from src.error_handlers import InvalidAPIUsage
from src.messages.api_error import APIError
from src.models.responces import permission_response
from src.service.permission import get_permission_service
from src.views.v1.api import api

from src.views.v1.api import get_resource_url, ResourceName

from src.service.decorators import admin_required

permission_ns = api.namespace(
    name='permissions',
    description='Operations with roles.',
    path=get_resource_url(ResourceName.PERMISSION)
)

service = get_permission_service()


@permission_ns.route('/')
class PermissionList(Resource):
    """
    Shows a list of all permissions, and lets you POST to add new permissions
    """

    @permission_ns.doc('list_permissions')
    @permission_ns.marshal_list_with(permission_response)
    @admin_required()
    def get(self):
        """List all permissions"""
        roles = service.filter_by()
        return roles

    @permission_ns.doc('create_permission')
    @permission_ns.marshal_with(permission_response)
    @admin_required()
    def post(self):
        """Create a new permissions"""
        if title := request.form.get('title', None):
            permission = service.add(title=title)
            if permission:
                return permission, HTTPStatus.CREATED
            raise InvalidAPIUsage(
                APIError.ALREADY_EXIST,
                status_code=HTTPStatus.NOT_ACCEPTABLE
            )
        raise InvalidAPIUsage(
            APIError.MISSING_PARAMETER,
            status_code=HTTPStatus.BAD_REQUEST
        )


@permission_ns.route('/<string:id>')
class PermissionUD(Resource):
    """Show a single permission item and lets you delete them"""

    @permission_ns.doc('get_permission')
    @permission_ns.marshal_with(permission_response)
    @admin_required()
    def get(self, id):
        """Fetch a given resource"""
        if permission := service.get(id):
            return permission
        raise InvalidAPIUsage(
            APIError.NOT_FOUND.value,
            status_code=HTTPStatus.NOT_FOUND
        )

    @permission_ns.doc('delete_role')
    @admin_required()
    def delete(self, id):
        """Delete a permission given its identifier"""
        if service.delete(id):
            return {}, HTTPStatus.OK
        raise InvalidAPIUsage(
            APIError.NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )

    @permission_ns.doc('update_role')
    @permission_ns.expect(permission_response)
    @permission_ns.marshal_with(permission_response)
    @admin_required()
    def put(self, id):
        """Update a permission given its identifier"""
        if permission := service.update(api.payload):
            return permission, HTTPStatus.OK
        raise InvalidAPIUsage(
            APIError.NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )
