from http import HTTPStatus
from unittest.mock import patch

from src.messages.api_error import APIError
from src.messages.api_error import get_error_response
from src.views.v1.api import get_resource_url, ResourceName
from tests.test_data.tokens import api_key_headers
from tests.test_data.user import TEST_USERS, TEST_USERS_RESPONSE

URL_PREFIX = get_resource_url(ResourceName.USER)


@patch('src.service.user.UserService.filter_by')
def test_user_list(filter_by_mock, test_client):
    filter_by_mock.return_value = TEST_USERS
    response = test_client.get(
        f'{URL_PREFIX}/',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert filter_by_mock.call_count == 1
    assert response.json == TEST_USERS_RESPONSE


@patch('src.service.user.UserService.get')
def test_user_by_id(get_mock, test_client):
    get_mock.return_value = TEST_USERS[0]
    response = test_client.get(
        f'{URL_PREFIX}/{TEST_USERS[0]["id"]}',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert get_mock.call_count == 1
    assert response.json == TEST_USERS_RESPONSE[0]


@patch('src.service.user.UserService.get')
def test_user_by_id_not_found(get_mock, test_client):
    get_mock.return_value = None
    response = test_client.get(
        f'{URL_PREFIX}/{TEST_USERS[0]["id"]}',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert get_mock.call_count == 1
    assert response.json == get_error_response(
        HTTPStatus.NOT_FOUND,
        APIError.NOT_FOUND
    )
