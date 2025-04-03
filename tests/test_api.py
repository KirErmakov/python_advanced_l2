from http import HTTPStatus

import pytest
from requests.exceptions import HTTPError

from app.models.models import UserData, UserDataUpdate


@pytest.mark.positive
def test_get_users(api_client, users_list):
    """Тест получения списка пользователей"""
    users = api_client.get_users()

    assert isinstance(users, list), "Response is not a list"
    assert len(users) > 0, "User list is empty"
    assert all(isinstance(user, UserData) for user in users), "Not all items are UserData"
    assert len(users) == len(users_list['items']), "Mismatch with direct user list"


@pytest.mark.positive
def test_get_user(api_client, fill_test_data):
    """Тест получения конкретного пользователя"""
    for user_id in fill_test_data:
        user = api_client.get_user(user_id)
        assert user.id == user_id


@pytest.mark.negative
@pytest.mark.parametrize('user_id', [9999])
def test_get_not_existing_user(api_client, user_id):
    """Тест обработки несуществующего пользователя"""
    with pytest.raises(HTTPError) as exc_info:
        api_client.get_user(user_id)

    assert exc_info.value.response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.negative
@pytest.mark.parametrize('user_id', [0, -1])
def test_get_user_invalid_id(api_client, user_id):
    """Тест 422 при передаче некорректного ID"""
    with pytest.raises(HTTPError) as exc_info:
        api_client.get_user(user_id)

    assert exc_info.value.response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.positive
def test_no_duplicated_users(api_client, users_list):
    """Тест на отсутствие дубликатов"""
    users = api_client.get_users()
    user_ids = [user.id for user in users]
    assert len(user_ids) == len(set(user_ids)), "Duplicate user IDs found"


@pytest.mark.positive
def test_create_user(api_client, test_user):
    """Тест создания пользователя"""
    created_user = api_client.create_user(test_user)

    assert created_user.id is not None, "Created user has no ID"
    assert created_user.email == test_user.email
    assert created_user.first_name == test_user.first_name
    assert created_user.last_name == test_user.last_name
    assert created_user.avatar == str(test_user.avatar)


@pytest.mark.positive
def test_update_user(api_client, create_user):
    """Тест обновления пользователя"""
    user_id = create_user
    update_data = UserDataUpdate(
        first_name="UpdatedName",
        email="updated@example.com",
        last_name="UpdatedLastName"
    )
    updated_user = api_client.update_user(user_id, update_data)

    assert updated_user.first_name == "UpdatedName"
    assert updated_user.email == "updated@example.com"
    assert updated_user.last_name == "UpdatedLastName"


@pytest.mark.positive
def test_delete_user(api_client, temp_user):
    """Тест удаления пользователя"""
    user_id = temp_user

    assert api_client.delete_user(user_id) is True, "User was not deleted"

    # Проверяем, что пользователь действительно удалён
    with pytest.raises(HTTPError) as exc_info:
        api_client.get_user(user_id)
    assert exc_info.value.response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.smoke
def test_status(api_client):
    """Smoke-тест: проверка доступности API"""
    response = api_client.get_status()
    assert response.status_code == 200, "API is not available"
