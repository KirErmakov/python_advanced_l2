import requests
import pytest
from http import HTTPStatus


@pytest.mark.smoke
def test_get_app_status(api_client):
    response = api_client.get_status()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'database': True}, 'Список пользователей пуст'


@pytest.mark.smoke
@pytest.mark.parametrize('method', ['post', 'put', 'delete'])
def test_method_not_allowed(api_client, method):
    request_method = getattr(api_client.session, method)
    response = request_method('/status')

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json().get('detail') == 'Method Not Allowed', 'Некорректное сообщение об ошибке'
