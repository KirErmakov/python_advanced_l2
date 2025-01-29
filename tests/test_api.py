import json
import pytest
import requests
from http import HTTPStatus

from app.models.models import UserData, UserDataUpdate


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
def test_get_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
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


@pytest.mark.positive
def test_create_user(app_url, test_user):
    response = requests.post(f'{app_url}/api/users/', json=test_user)
    assert response.status_code == HTTPStatus.CREATED

    created_user = response.json()
    UserData.model_validate(created_user)
    assert created_user['email'] == test_user['email']


@pytest.mark.positive
@pytest.mark.parametrize('email', ['new_email@gmail.com'])
def test_update_user(app_url, create_user, email):
    update_info = {'email': email}
    response = requests.patch(f'{app_url}/api/users/{create_user}', json=update_info)
    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    UserDataUpdate.model_validate(updated_user)
    assert updated_user['email'] == update_info['email']


@pytest.mark.positive
def test_delete_user(app_url, create_user):
    response = requests.delete(f'{app_url}/api/users/{create_user}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User deleted'

