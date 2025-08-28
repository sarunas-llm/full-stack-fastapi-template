from sqlmodel import Session

from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_lower_string


def test_create_product_requires_superuser(
    client, normal_user_token_headers, db: Session
) -> None:
    category = create_random_category(db)
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "price": 1.0,
        "category_id": str(category.id),
    }
    response = client.post(
        "/api/v1/products/", headers=normal_user_token_headers, json=data
    )
    assert response.status_code == 403


def test_crud_product(client, superuser_token_headers, db: Session) -> None:
    category = create_random_category(db)
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "price": 1.0,
        "category_id": str(category.id),
    }
    response = client.post(
        "/api/v1/products/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    product = response.json()
    product_id = product["id"]

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200

    update = {"name": random_lower_string()}
    response = client.put(
        f"/api/v1/products/{product_id}",
        headers=superuser_token_headers,
        json=update,
    )
    assert response.status_code == 200

    response = client.delete(
        f"/api/v1/products/{product_id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
