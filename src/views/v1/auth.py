from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from src.error_handlers import InvalidAPIUsage
from src.messages.error import AuthError
from src.service.auth import AuthService
from src.utils import make_success_response
from src.views.v1.api import api
from src.views.v1.api import get_resource_url, ResourceName

access_ns = api.namespace(
    'access',
    description='Access operations.',
    path=get_resource_url(ResourceName.AUTH),
)


@access_ns.route('/signup')
class Signup(Resource):
    @access_ns.doc('user_signup')
    def post(self):
        errors = []

        if not request.form.get('pwd'):
            errors.append(AuthError.MISSING_PWD)
        if not request.form.get('login'):
            errors.append(AuthError.MISSING_LOGIN)

        if errors:
            raise InvalidAPIUsage(','.join(errors),
                                  status_code=HTTPStatus.BAD_REQUEST)

        auth = AuthService(
            pwd=request.form.get('pwd'),
            username=request.form.get('login')
        )
        user_id = auth.signup()

        if not user_id:
            raise InvalidAPIUsage(AuthError.USER_EXISTED,
                                  status_code=HTTPStatus.UNAUTHORIZED)

        return make_success_response({'user_id': user_id})


@access_ns.route('/login')
class login(Resource):
    def post(self):
        errors = []

        if not request.form.get('login'):
            errors.append(AuthError.MISSING_LOGIN)
        if not request.form.get('pwd'):
            errors.append(AuthError.MISSING_PWD)
        if errors:
            raise InvalidAPIUsage(','.join(errors),
                                  status_code=HTTPStatus.BAD_REQUEST)

        auth = AuthService(
            pwd=request.form.get('pwd'),
            username=request.form.get('login'),
            agent=request.headers.get('User-Agent'),
        )
        tokens = auth.login()
        if not tokens:
            raise InvalidAPIUsage(AuthError.USER_NOT_FOUND,
                                  status_code=HTTPStatus.UNAUTHORIZED)

        return make_success_response(tokens)


@access_ns.route('/user')
class ProfileUser(Resource):
    def get(self):
        errors = []
        if not request.headers.get('Access-Token'):
            errors.append(AuthError.NO_ACCESS_TOKEN)

        if not request.headers.get('Refresh-Token'):
            errors.append(AuthError.NO_REFRESH_TOKEN)

        if errors:
            raise InvalidAPIUsage(','.join(errors),
                                  status_code=HTTPStatus.BAD_REQUEST)

        auth = AuthService(
            '',
            '',
            agent=request.headers.get('User-Agent'),
        )
        args = auth.get_session(
            request.headers.get('Access-Token'),
            request.headers.get('Refresh-Token')
        )

        if not args:
            raise InvalidAPIUsage(AuthError.EXPIRED_TOKENS,
                                  status_code=HTTPStatus.UNAUTHORIZED)

        return make_success_response(args)


@access_ns.route('/logout')
class Logout(Resource):
    def get(self):
        errors = []
        if not request.headers.get('Access-Token'):
            errors.append(AuthError.NO_ACCESS_TOKEN)

        if not request.headers.get('Refresh-Token'):
            errors.append(AuthError.NO_REFRESH_TOKEN)

        if errors:
            raise InvalidAPIUsage(','.join(errors),
                                  status_code=HTTPStatus.BAD_REQUEST)

        auth = AuthService('', '')
        auth.logout(
            request.headers.get('Access-Token'),
            request.headers.get('Refresh-Token')
        )

        return make_success_response('Logout is successful')
