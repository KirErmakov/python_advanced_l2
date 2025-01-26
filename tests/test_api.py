import pytest
import requests
from http import HTTPStatus
from models import UserData


@pytest.fixture
def users_list(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.mark.positive
def test_get_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK, "Неверный HTTP статус-код"

    data = response.json()
    assert "items" in data, "Отсутствует ключ 'items' в ответе"
    assert "total" in data, "Отсутствует ключ 'total' в ответе"
    assert "page" in data, "Отсутствует ключ 'page' в ответе"
    assert "size" in data, "Отсутствует ключ 'size' в ответе"

    for user in data['items']:
        UserData.model_validate(user)


def test_no_duplicated_users(users_list):
    users_ids = [item['id'] for item in users_list['items']]

    assert len(users_ids) == len(set(users_ids))


@pytest.mark.positive
@pytest.mark.parametrize('user_id', [1, 6, 12])
def test_get_user(app_url, user_id):
    response = requests.get(url=f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK
    user = response.json()
    UserData.model_validate(user)


@pytest.mark.negative
@pytest.mark.parametrize('user_id', [13, 20])
def test_get_not_existing_user(app_url, user_id):
    response = requests.get(url=f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.negative
@pytest.mark.parametrize("user_id", [-1, 0, "abc1%"])
def test_get_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


