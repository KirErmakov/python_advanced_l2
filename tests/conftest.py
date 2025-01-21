import pytest

REQRES_URL = "https://reqres.in"
MY_SERVICE_URL = "http://127.0.0.1:8000"

USERS_API = "/api/users"
REGISTER_API = "/api/register"


@pytest.fixture(params=[REQRES_URL, MY_SERVICE_URL])
def domain_url(request):
    return request.param

@pytest.fixture()
def base_endpoint(domain_url):
    base_endpoint = f"{domain_url}{USERS_API}"
    register_endpoint = f"{domain_url}{REGISTER_API}"

    return base_endpoint, register_endpoint
