from http import HTTPStatus
from unittest.mock import patch

from src.messages.api_error import APIError
from src.messages.api_error import get_error_response
from src.views.v1.api import get_resource_url, ResourceName
from tests.test_data.permission import TEST_PERMISSIONS
from tests.test_data.permission import TEST_PERMISSIONS_RESPONSE
from tests.test_data.tokens import api_key_headers

URL_PREFIX = get_resource_url(ResourceName.PERMISSION)


@patch('src.service.permission.PermissionService.get')
def test_permission_delete_not_exist(get_mock, test_client):
    get_mock.return_value = None
    response = test_client.delete(
        f'{URL_PREFIX}/{TEST_PERMISSIONS[0].id}',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert get_mock.call_count == 1
    assert response.json == get_error_response(
        HTTPStatus.NOT_FOUND,
        APIError.NOT_FOUND,
    )


@patch('src.service.permission.PermissionService.create')
@patch('src.service.permission.PermissionService.get_by')
def test_permission_create_new(get_by_mock, create_mock, test_client):
    get_by_mock.return_value = None
    create_mock.return_value = TEST_PERMISSIONS[0]
    response = test_client.post(
        f'{URL_PREFIX}/',
        data={
            'title': TEST_PERMISSIONS[0].title,
        },
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert get_by_mock.call_count == 1
    assert create_mock.call_count == 1
    assert response.json == TEST_PERMISSIONS_RESPONSE[0]


@patch('src.service.permission.PermissionService.get_by')
def test_permission_create_already_exist(get_by_mock, test_client):
    get_by_mock.return_value = TEST_PERMISSIONS[0]
    response = test_client.post(
        f'{URL_PREFIX}/',
        data={
            'title': TEST_PERMISSIONS[0].title,
        },
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE
    assert get_by_mock.call_count == 1
    assert response.json == get_error_response(
        HTTPStatus.NOT_ACCEPTABLE,
        APIError.ALREADY_EXIST,
    )


def test_permission_create_missing_parameter(test_client):
    response = test_client.post(
        f'{URL_PREFIX}/',
        data={},
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == get_error_response(
        HTTPStatus.BAD_REQUEST,
        APIError.MISSING_PARAMETER,
    )


@patch('src.service.permission.PermissionService.filter_by')
def test_permission_list(filter_by_mock, test_client):
    filter_by_mock.return_value = TEST_PERMISSIONS
    response = test_client.get(
        f'{URL_PREFIX}/',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert filter_by_mock.call_count == 1
    assert response.json == TEST_PERMISSIONS_RESPONSE


@patch('src.service.permission.PermissionService.get')
def test_permission_by_id(get_mock, test_client):
    get_mock.return_value = TEST_PERMISSIONS[0]
    response = test_client.get(
        f'{URL_PREFIX}/{TEST_PERMISSIONS[0].id}',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert get_mock.call_count == 1
    assert response.json == TEST_PERMISSIONS_RESPONSE[0]


@patch('src.service.permission.PermissionService.get')
def test_permission_by_id_not_found(get_mock, test_client):
    get_mock.return_value = None
    response = test_client.get(
        f'{URL_PREFIX}/{TEST_PERMISSIONS[0].id}',
        headers=api_key_headers,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert get_mock.call_count == 1
    assert response.json == get_error_response(
        HTTPStatus.NOT_FOUND,
        APIError.NOT_FOUND
    )
