from sqlmodel import Session

from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_lower_string


def test_create_category_requires_superuser(client, normal_user_token_headers) -> None:
    data = {"name": random_lower_string(), "description": random_lower_string()}
    response = client.post(
        "/api/v1/categories/", headers=normal_user_token_headers, json=data
    )
    assert response.status_code == 403


def test_crud_category(client, superuser_token_headers) -> None:
    data = {"name": random_lower_string(), "description": random_lower_string()}
    response = client.post(
        "/api/v1/categories/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    category = response.json()
    category_id = category["id"]

    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200

    update = {"name": random_lower_string()}
    response = client.put(
        f"/api/v1/categories/{category_id}",
        headers=superuser_token_headers,
        json=update,
    )
    assert response.status_code == 200

    response = client.delete(
        f"/api/v1/categories/{category_id}", headers=superuser_token_headers
    )
    assert response.status_code == 200


def test_delete_category_with_products_fails(
    client, superuser_token_headers, db: Session
) -> None:
    product = create_random_product(db)
    category_id = product.category_id
    response = client.delete(
        f"/api/v1/categories/{category_id}", headers=superuser_token_headers
    )
    assert response.status_code == 400
