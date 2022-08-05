from http import HTTPStatus

import pytest
from src.messages.api_error import APIError

from app import app


@pytest.fixture(scope='session')
def test_client():
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
