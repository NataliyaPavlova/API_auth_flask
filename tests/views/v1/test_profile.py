from http import HTTPStatus

from src.messages.error import ProfileError
from src.views.v1.api import get_resource_url, ResourceName

URL_PREFIX = get_resource_url(ResourceName.PROFILE)


def test_change_no_new_data(test_client):
    response = test_client.post(
        f'{URL_PREFIX}/change',
        data={'login': 'testuser'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == ProfileError.NO_INFO_TO_CHANGE


def test_history_missing_field(test_client):
    response = test_client.get(
        f'{URL_PREFIX}/history',
        data={
            'login': '',
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == ProfileError.MISSING_LOGIN
