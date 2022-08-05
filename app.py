import click
from flask import Flask

from src.error_handlers import InvalidAPIUsage
from src.service.auth import AuthService
from src.service.role import get_role_service
from src.storages.db_connect import init_db
from src.views.v1.api import api
from src.views.v1.auth import access_ns
from src.views.v1.permissions import permission_ns
from src.views.v1.profile import profile_ns
from src.views.v1.roles import role_ns
from src.views.v1.users import user_ns

app = Flask(__name__)

api.add_namespace(permission_ns)
api.add_namespace(role_ns)
api.add_namespace(user_ns)
api.add_namespace(profile_ns)
api.add_namespace(access_ns)

api.init_app(app)


@app.cli.command('create_superuser')
@click.argument('password')
def create_user(password: str):
    role_service = get_role_service()
    admin_role = role_service.create(
        title='Administrator'
    )
    if not admin_role:
        print('Error. Can create role.')
        return False

    auth = AuthService(
        pwd=password,
        username='administrator',
        role_id=admin_role.id,
    )
    user_id = auth.signup()
    if not user_id:
        print('Error. Can create superuser.')
        return False

    print('Superuser created.')


@api.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    result = e.answer
    return result, e.status_code


init_db(app)
app.app_context().push()
