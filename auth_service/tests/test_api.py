import pytest

from auth_service.app.security import hash_password, verify_password


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test@example.com"
    assert "id" in data["user"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "test@example.com",
        "password": "password123",
    }

    first_response = await client.post(
        "/register",
        json=payload
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/register",
        json=payload
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_register_short_password(client):
    response = await client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "123",
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login(client):
    payload = {
        "email": "test@example.com",
        "password": "password123",
    }

    register_response = await client.post(
        "/register",
        json=payload
    )

    assert register_response.status_code == 201

    response = await client.post(
        "/login",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test@example.com"
    assert "id" in data["user"]


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post(
        "/login",
        json={
            "email": "unknown@example.com",
            "password": "password123",
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User doesn't exist"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        }
    )

    response = await client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        }
    )

    assert response.status_code == 401