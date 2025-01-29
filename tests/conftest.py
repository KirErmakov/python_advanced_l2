import os
import json
import requests
import dotenv
import pytest
from http import HTTPStatus
from faker import Faker



@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope='session')
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture(scope='session')
def fill_test_data(app_url):
    with open("../users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user['id'] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture
def users_list(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


fake = Faker()

@pytest.fixture
def test_user() -> dict:
    test_user = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'avatar': fake.image_url()
    }
    return test_user

@pytest.fixture
def create_user(app_url, test_user) -> int:
    new_user = requests.post(f'{app_url}/api/users/', json=test_user)
    return new_user.json()['id']
