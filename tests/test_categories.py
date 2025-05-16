# tests/test_categories.py
import pytest
from fastapi import status
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

def test_read_categories(client, test_category):
    response = client.get("/categories/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_read_category(client, test_category):
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_category.id

def test_create_category(client, admin_token):
    category_data = {"name": "New Category"}
    response = client.post(
        "/categories/",
        json=category_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == category_data["name"]

def test_update_category(client, admin_token, test_category):
    update_data = {"name": "Updated Category"}
    response = client.put(
        f"/categories/{test_category.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == update_data["name"]

def test_delete_category(client, admin_token, test_category):
    response = client.delete(
        f"/categories/{test_category.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify category is deleted
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND