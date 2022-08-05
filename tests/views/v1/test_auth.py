from http import HTTPStatus
from unittest.mock import patch

from src.messages.error import AuthError
from src.service.token import Token
from src.views.v1.api import get_resource_url, ResourceName
from tests.test_data.auth import TESTUSER, NEWUSER

URL_PREFIX = get_resource_url(ResourceName.AUTH)


def test_signup_missing_field(test_client):
    response = test_client.post(
        f'{URL_PREFIX}/signup',
        data={'login': 'testuser'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == AuthError.MISSING_PWD

    response = test_client.post(
        f'{URL_PREFIX}/signup',
        data={'pwd': 'aaa'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == AuthError.MISSING_LOGIN


@patch('src.service.user.UserService.get_by')
def test_signup_existed_user(dbsession_query_mock, test_client):
    dbsession_query_mock.return_value = TESTUSER

    response = test_client.post(
        f'{URL_PREFIX}/signup',
        data={'login': 'existing_user', 'pwd': 'aaa'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json['message'] == AuthError.USER_EXISTED


@patch('src.service.user.UserService.create')
@patch('src.service.user.UserService.get_by')
def test_signup_success(dbsession_query_mock, dbsession_create_mock,
                        test_client):
    dbsession_query_mock.return_value = None
    dbsession_create_mock.return_value = NEWUSER

    response = test_client.post(
        f'{URL_PREFIX}/signup',
        data={'login': 'new_user', 'pwd': 'password'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'response': 'success',
        'result': {
            'user_id': '32dea17d-7b0c-4639-8c4e-e4be818e8aaf'
        },
        'status': 200
    }


def test_login_missing_field(test_client):
    response = test_client.post(
        f'{URL_PREFIX}/login',
        data={'login': 'testuser'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == AuthError.MISSING_PWD

    response = test_client.post(
        f'{URL_PREFIX}/login',
        data={'pwd': 'aaa'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == AuthError.MISSING_LOGIN


@patch('src.service.user.UserService.get_by', return_value=False)
def test_login_non_existed_user(dbsession_query_mock, test_client):
    dbsession_query_mock.return_value = []

    response = test_client.post(
        f'{URL_PREFIX}/login',
        data={'login': 'non_existing_user', 'pwd': 'aaa'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json['message'] == AuthError.USER_NOT_FOUND


@patch('src.service.user.UserService.get_by')
def test_login_incorrect_pwd(dbsession_query_mock, test_client):
    dbsession_query_mock.return_value = TESTUSER

    response = test_client.post(
        f'{URL_PREFIX}/login',
        data={'login': 'existing_user', 'pwd': 'incorrect_password'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json['message'] == AuthError.USER_NOT_FOUND


@patch('src.service.token.Token.new')
@patch('src.service.history.HistoryService.create')
@patch('src.service.user.UserService.get_by')
def test_login_success(dbsession_query_mock, history_create_mock, token_mock,
                       test_client):
    dbsession_query_mock.return_value = TESTUSER
    history_create_mock.return_value = False
    token_mock.return_value = 'proper_token'

    response = test_client.post(
        f'{URL_PREFIX}/login',
        data={'login': 'existing_user', 'pwd': 'password'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'response': 'success',
        'result': {
            'Access-Token': 'proper_token',
            'Refresh-Token': 'proper_token'
        },
        'status': 200
    }


@patch('src.service.token.Token.get_user_id')
@patch('src.service.token.Token.is_valid')
@patch('src.service.history.HistoryService.create')
def test_profile_success(history_create_mock, token_valid_mock,
                         token_get_user_id, test_client):
    history_create_mock.return_value = False
    token_valid_mock.return_value = True
    token_get_user_id.return_value = 'test_user_id'

    response = test_client.get(
        f'{URL_PREFIX}/user',
        headers={'Access-Token': 'access', 'Refresh-Token': 'refresh'},
        data={},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'response': 'success',
        'result': {
            'Access-Token': 'access',
            'Refresh-Token': 'refresh'
        },
        'status': 200
    }


@patch.object(Token, 'is_valid', False)
def test_profile_expired_token(test_client):
    response = test_client.get(
        f'{URL_PREFIX}/user',
        headers={'Access-Token': 'expired', 'Refresh-Token': 'expired'},
        data={},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json['message'] == AuthError.EXPIRED_TOKENS


@patch.object(Token, 'is_valid', True)
@patch('src.service.token.Token.get_payload')
@patch('src.service.token.redis_client')
def test_logout_success(redis_mock, get_payload_mock, test_client):
    redis_mock.set.return_value = True
    get_payload_mock.return_value = {'user_id': 'testuser'}
    response = test_client.get(
        f'{URL_PREFIX}/logout',
        headers={'Access-Token': 'valid', 'Refresh-Token': 'valid'},
        data={},
    )
    assert response.status_code == HTTPStatus.OK
    assert redis_mock.set.call_count == 1
