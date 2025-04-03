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
@pytest.mark.positive
@pytest.mark.usefixtures("fill_test_data")
def test_pagination(api_client, page, size):
    """Тест базовой пагинации: items, total, page, size"""
    response = api_client.session.get("/api/users", params={'page': page, 'size': size})
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "items" in data, "Missing 'items'"
    assert "total" in data, "Missing 'total'"
    assert "page" in data, "Missing 'page'"
    assert "size" in data, "Missing 'size'"

    assert len(data["items"]) == size, f"Expected page size {size}, got {len(data['items'])}"
    assert data["page"] == page, f"Expected page {page}, got {data['page']}"
    assert data["size"] == size, f"Expected size {size}, got {data['size']}"


@pytest.mark.parametrize("size", [1, 2, 6, 11, 12, 13])
@pytest.mark.positive
@pytest.mark.usefixtures("fill_test_data")
def test_pagination_total_pages(api_client, size):
    """Проверка правильного расчета общего количества страниц"""
    response = api_client.session.get("/api/users", params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    total_items = data['total']
    expected_pages = ceil(total_items / size)

    assert "pages" in data, "Missing 'pages'"
    assert data['pages'] == expected_pages, \
        f"Expected pages {expected_pages}, got {data['pages']}"


@pytest.mark.parametrize("start_page,size,num_pages", [
    (1, 4, 3),
    (1, 3, 4)
])
@pytest.mark.positive
@pytest.mark.usefixtures("fill_test_data")
def test_pagination_unique_data(api_client, start_page, size, num_pages):
    """Проверка уникальности данных на страницах"""
    response = api_client.session.get("/api/users", params={'page': start_page, 'size': size})
    assert response.status_code == HTTPStatus.OK

    previous_data = response.json()["items"]
    previous_ids = {item["id"] for item in previous_data}

    for page in range(start_page + 1, start_page + num_pages):
        response = api_client.session.get("/api/users", params={'page': page, 'size': size})
        assert response.status_code == HTTPStatus.OK

        current_data = response.json()["items"]
        current_ids = {item["id"] for item in current_data}

        assert not previous_ids.intersection(current_ids), \
            f"Page {page} has duplicate IDs with page {page - 1}"

        previous_ids = current_ids
