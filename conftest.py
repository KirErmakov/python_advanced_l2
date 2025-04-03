import os
import json
import dotenv
import pytest
from faker import Faker

from app.clients.UserApi import UserApi
from app.models.models import UserDataCreate, UserData
from utils.path import get_file_path

pytest_plugins = ['fixture_session']


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="rc",
        help="Environment: dev or rc"
    )


@pytest.fixture(scope="session")
def env(request):
    env_value = request.config.getoption("--env")
    return env_value


@pytest.fixture(scope="session")
def reqres_session(env):
    from config import Server
    from utils.base_session import BaseSession
    base_url = Server(env).reqres
    print(f"[BASE URL] Using API at: {base_url}")
    with BaseSession(base_url=base_url) as session:
        yield session


@pytest.fixture(scope='session')
def api_client(reqres_session):
    """Фикстура возвращает готовый клиент для работы с API"""
    return UserApi(session=reqres_session)


@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope='session')
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope='session')
def fill_test_data(api_client):
    json_path = get_file_path('users.json')
    with open(json_path) as f:
        test_data_users = json.load(f)

    created_users = []
    for user_data in test_data_users:
        user_data_model = UserDataCreate(**user_data)
        new_user = api_client.create_user(user_data_model)
        created_users.append(new_user)

    user_ids = [user.id for user in created_users]
    yield user_ids

    for user_id in user_ids:
        api_client.delete_user(user_id)


@pytest.fixture
def users_list(api_client):
    users = api_client.get_users()
    return {
        'items': users,
        'total': len(users)
    }


fake = Faker()


@pytest.fixture
def test_user() -> UserDataCreate:
    test_user = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'avatar': fake.image_url()
    }
    return UserDataCreate(**test_user)


@pytest.fixture
def create_user(api_client, test_user: UserDataCreate):
    new_user = api_client.create_user(test_user)

    yield new_user.id

    api_client.delete_user(new_user.id)

@pytest.fixture
def temp_user(api_client, test_user: UserDataCreate):
    """Временный пользователь без автоудаления — используется в тесте удаления"""
    new_user = api_client.create_user(test_user)
    return new_user.id
