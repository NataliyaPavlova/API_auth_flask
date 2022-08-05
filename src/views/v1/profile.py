from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from src.error_handlers import InvalidAPIUsage
from src.messages.error import ProfileError
from src.models.db_models import History
from src.models.requests import only_login_request
from src.models.requests import profile_change_request
from src.models.responces import user_response
from src.service.auth import AuthService
from src.utils import make_success_response
from src.views.v1.api import api
from src.views.v1.api import get_resource_url, ResourceName

profile_ns = api.namespace(
    'profile',
    description='Operations with user profile.',
    path=get_resource_url(ResourceName.PROFILE),
)


@profile_ns.route('/change')
class ProfileChange(Resource):
    @profile_ns.doc('profile_change')
    @profile_ns.marshal_list_with(user_response)
    @profile_ns.expect(profile_change_request)
    def post(self):
        errors = []

        if not request.form.get('login', None):
            errors.append(ProfileError.MISSING_LOGIN)
        if not request.form.get('new_pwd', None) and not request.form.get(
                'new_login', None):
            errors.append(ProfileError.NO_INFO_TO_CHANGE)

        if errors:
            raise InvalidAPIUsage(','.join(errors),
                                  status_code=HTTPStatus.BAD_REQUEST)

        auth = AuthService(
            pwd='',
            username=request.form.get('login')
        )
        user = auth.change(
            pwd=request.form.get('new_pwd'),
            login=request.form.get('new_login')
        )
        if not user:
            raise InvalidAPIUsage(ProfileError.USER_EXISTED.value,
                                  status_code=HTTPStatus.BAD_REQUEST)

        return make_success_response({'user': str(user.login)})


@profile_ns.route('/history')
class HistoryResource(Resource):
    @profile_ns.doc('profile_change')
    @profile_ns.expect(only_login_request)
    def get(self):
        errors = []

        if not request.form.get('login', None):
            errors.append(ProfileError.MISSING_LOGIN)

        if errors:
            raise InvalidAPIUsage(ProfileError.MISSING_LOGIN,
                                  status_code=HTTPStatus.BAD_REQUEST)
        auth = AuthService(
            pwd='',
            username=request.form.get('login', None)
        )

        auth_history = auth.get_history()
        prepared = History.query_prepared_to_json(auth_history)
        return prepared
