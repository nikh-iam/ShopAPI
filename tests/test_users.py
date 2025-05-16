# tests/test_users.py
from datetime import datetime
import pytest
from fastapi import status
from app.schemas.user_schema import UserCreate, UserUpdate

def test_register_user(client, db_session):
    user_data = {
        "email": f"newuser_{datetime.now().timestamp()}@example.com",
        "password": "newpassword",
        "first_name": "New",
        "last_name": "User",
        "phone_no": "1234567890"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()

def test_register_existing_email(client, test_user):
    user_data = {
        "email": test_user.email,
        "password": "password",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_user(client, test_user):
    response = client.post(
        "/users/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    response = client.post(
        "/users/login",
        data={"username": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_read_user_me(client, user_token):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.json()

def test_update_user_me(client, user_token, db_session):
    update_data = {"first_name": "Updated"}
    response = client.put(
        "/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Updated"

def test_delete_user_me(client, user_token, db_session):
    response = client.delete(
        "/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify user is deleted
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_admin_read_users(client, admin_token, test_user):
    response = client.get(
        "/users/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_admin_read_user_by_id(client, admin_token, test_user):
    response = client.get(
        f"/users/{test_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_user.id

def test_admin_update_user(client, admin_token, test_user):
    update_data = {"is_active": False}
    response = client.put(
        f"/users/{test_user.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_user.id

def test_admin_delete_user(client, admin_token, test_user, db_session):
    response = client.delete(
        f"/users/{test_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verify user is deleted
    response = client.get(
        f"/users/{test_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND