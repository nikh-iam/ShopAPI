# tests/test_products.py
import pytest
from fastapi import status
from app.schemas.product_schema import ProductCreate, ProductUpdate

def test_read_products(client, test_product):
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_read_product(client, test_product):
    response = client.get(f"/products/{test_product.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_product.id

def test_read_nonexistent_product(client):
    response = client.get("/products/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_product(client, admin_token, test_category):
    product_data = {
        "title": "New Product",
        "description": "New Description",
        "price": 19.99,
        "category_id": test_category.id,
        "stock": 50
    }
    response = client.post(
        "/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == product_data["title"]

def test_create_product_unauthorized(client, test_category):
    product_data = {
        "title": "New Product",
        "description": "New Description",
        "price": 19.99,
        "category_id": test_category.id,
        "stock": 50
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_product(client, admin_token, test_product):
    update_data = {"price": 15.99}
    response = client.put(
        f"/products/{test_product.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["price"] == 15.99

def test_delete_product(client, admin_token, test_product):
    response = client.delete(
        f"/products/{test_product.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify product is deleted
    response = client.get(f"/products/{test_product.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_products(client, test_product):
    response = client.get("/products/search/?search=Test")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_search_products_by_price_range(client, test_product):
    response = client.get("/products/search/?min_price=5&max_price=15")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0