import pytest
import requests
from data import register_user


@pytest.mark.positive
def test_register_successful(base_endpoint):
    response = requests.post(url=base_endpoint[1], json=register_user)

    assert response.status_code == 200
    assert 'id' in response.json() and 'token' in response.json()


@pytest.mark.negative
def test_register_non_password(base_endpoint):
    response = requests.post(url=base_endpoint[1], json={"email": register_user["email"]})

    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()["error"] == "Missing password"


@pytest.mark.negative
def test_register_non_email(base_endpoint):
    response = requests.post(url=base_endpoint[1], json={"password": register_user["password"]})

    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()["error"] == "Missing email or username"
