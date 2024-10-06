from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
USER_CLIENT = pytest.lazy_fixture('client')
READER_CLIENT = pytest.lazy_fixture('reader_client')


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        (HOME_URL, USER_CLIENT, HTTPStatus.OK),
        (LOGIN_URL, USER_CLIENT, HTTPStatus.OK),
        (DETAIL_URL, USER_CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, USER_CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, USER_CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, READER_CLIENT, HTTPStatus.NOT_FOUND),
    ),
)
def test_availability(name, parametrized_client, expected_status):
    response = parametrized_client.get(name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name', (EDIT_URL, DELETE_URL,))
def test_redirect_for_anonymous_client(client, login_url, name,):
    expected_url = f'{login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
