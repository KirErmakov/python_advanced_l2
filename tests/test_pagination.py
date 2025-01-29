import requests
import pytest
from math import ceil
from http import HTTPStatus



@pytest.mark.parametrize("page,size", [
    (1, 12),
    (2, 6),
    (3, 4),
    (4, 3),
    (6, 2)
])
@pytest.mark.usefixtures("fill_test_data")
def test_pagination(app_url, page, size):
    params = {'page': page, 'size': size}
    response = requests.get(f"{app_url}/api/users", params=params)

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "items" in data, "Отсутствует ключ 'items' в ответе"
    assert "total" in data, "Отсутствует ключ 'total' в ответе"

    assert len(data['items']) == size, f"Размер страницы превышает ожидаемое (size={size})"
    assert data['page'] == page, f"Неверный номер страницы: {data['page']} вместо {page}"
    assert data['size'] == size, f"Неверный размер страницы: {data['page']} вместо {size}"


@pytest.mark.parametrize("size", [1, 2, 6, 11, 12, 13])
@pytest.mark.usefixtures("fill_test_data")
def test_pagination_total_pages(app_url, size):
    response = requests.get(f"{app_url}/api/users", params={"page": 1, "size": size})
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    total_items = data['total']
    expected_pages = ceil(total_items / size)
    assert data['pages'] == expected_pages, \
        f"Ожидамое кол-во страниц - {expected_pages}, фактическое - {data['pages']}"


@pytest.mark.parametrize("start_page,size,num_pages", [
    (1, 4, 3),
    (1, 3, 4)
])
@pytest.mark.usefixtures("fill_test_data")
def test_pagination_unique_data(app_url, start_page, num_pages, size):
    response = requests.get(f"{app_url}/api/users", params={'page': start_page, 'size': size})
    assert response.status_code == HTTPStatus.OK
    previous_data = response.json()['items']
    prev_ids = {item['id'] for item in previous_data}

    for page in range(start_page + 1 , start_page + num_pages):
        params = {'page': page, 'size': size}
        response = requests.get(f"{app_url}/api/users", params=params)
        assert response.status_code == HTTPStatus.OK
        current_data = response.json()['items']
        curr_ids = {item['id'] for item in current_data}

        assert  curr_ids != prev_ids, \
                f"Данные на странице {page} совпадают с данными на странице {page - 1}"

        prev_ids = curr_ids
