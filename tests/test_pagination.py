import requests
import pytest
from http import HTTPStatus

@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 10),
    (3, 20),
    (1, 50),
    (5, 5)
])
def test_pagination(app_url, page, size):
    params = {'page': page, 'size': size}
    response = requests.get(f"{app_url}/api/users", params=params)

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "items" in data, "Отсутствует ключ 'items' в ответе"
    assert "total" in data, "Отсутствует ключ 'total' в ответе"

    assert len(data['items']) <= size, f"Размер страницы превышает ожидаемое (size={size})"
    assert data['page'] == page, f"Неверный номер страницы: {data['page']} вместо {page}"
    assert data['size'] == size, f"Неверный размер страницы: {data['page']} вместо {size}"


@pytest.mark.parametrize("start_page,size,num_pages", [
    (1, 4, 3),
    (1, 3, 4)
])
def test_pagination_unique_data(app_url, start_page, num_pages, size):
    previous_data = None

    for page in range(start_page, start_page + num_pages):
        params = {'page': page, 'size': size}
        response = requests.get(f"{app_url}/api/users", params=params)
        assert response.status_code == HTTPStatus.OK, "Неверный HTTP статус-код"

        current_data = response.json()['items']
        if previous_data is not None:
            assert current_data != previous_data, \
                f"Данные на странице {page} совпадают с данными на странице {page - 1}"

        previous_data = current_data
