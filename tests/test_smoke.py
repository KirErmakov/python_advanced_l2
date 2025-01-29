import requests
import pytest
from http import HTTPStatus


@pytest.mark.smoke
def test_get_app_status(app_url):
    response = requests.get(f'{app_url}/status')

    assert response.status_code == HTTPStatus.OK , 'Неверный HTTP-код ответа'
    assert response.json() == {'database': True}, 'Список пользователей пуст'



@pytest.mark.smoke
@pytest.mark.parametrize('method', ['post', 'put', 'delete'])
def test_method_not_allowed(app_url, method):
    request_method = getattr(requests, method)
    response = request_method(f'{app_url}/status')

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, 'Ожидается HTTP-код 405'
    assert response.json().get('detail') == 'Method Not Allowed', 'Сообщение об ошибке некорректно'
