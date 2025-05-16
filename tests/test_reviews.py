# tests/test_reviews.py
import pytest
from fastapi import status
from app.schemas.review_schema import ReviewCreate, ReviewUpdate

def test_create_review(client, user_token, test_product, test_order):
    review_data = {
        "product_id": test_product.id,
        "rating": 5,
        "comment": "Great product!"
    }
    response = client.post(
        "/reviews/",
        json=review_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["rating"] == 5

def test_get_reviews_by_product(client, test_review, test_product):
    response = client.get(f"/reviews/product/{test_product.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_update_review(client, user_token, test_review):
    update_data = {"rating": 4}
    response = client.put(
        f"/reviews/{test_review.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["rating"] == 4

def test_delete_review(client, user_token, test_review):
    response = client.delete(
        f"/reviews/{test_review.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify review is deleted
    response = client.get(f"/reviews/product/{test_review.product_id}")
    assert len(response.json()) == 0