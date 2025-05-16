# tests/test_cart.py
import pytest
from fastapi import status
from app.schemas.cart_schema import CartItemCreate

def test_read_cart(client, user_token, test_cart_item):
    response = client.get(
        "/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) > 0

def test_add_to_cart(client, user_token, test_product):
    item_data = {"product_id": test_product.id, "quantity": 1}
    response = client.post(
        "/cart/add",
        json=item_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) > 0

def test_update_cart_item(client, user_token, test_cart_item):
    response = client.put(
        f"/cart/update/{test_cart_item.id}?quantity=3", 
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["items"][0]["quantity"] == 3

def test_remove_from_cart(client, user_token, test_cart_item):
    response = client.delete(
        f"/cart/remove/{test_cart_item.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 0

def test_clear_cart(client, user_token, test_cart_item):
    response = client.delete(
        "/cart/clear",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify cart is empty
    response = client.get(
        "/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert len(response.json()["items"]) == 0