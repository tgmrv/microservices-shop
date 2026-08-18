import jwt
import pytest

from auth_service.app.config import settings
from auth_service.app.models import UserORM
from auth_service.app.security import create_access_token, verify_password, hash_password


@pytest.mark.asyncio
async def test_create_access_token():
    user = UserORM(
        id="user-123",
        email="test@example.com",
        hashed_password="hashed-password"
    )

    token = await create_access_token(user)

    payload = jwt.decode(
        token,
        key=settings.JWT_SECRET.get_secret_value(),
        algorithms=[settings.JWT_ALGORITHM],
    )

    assert payload["user_id"] == "user-123"
    assert payload["email"] == "test@example.com"
    assert payload["role"] == "user"
    assert "exp" in payload


@pytest.mark.asyncio
async def test_hash_password():
    password = "password123"

    hashed = await hash_password(password)

    assert hashed != password
    assert await verify_password(password, hashed)


@pytest.mark.asyncio
async def test_verify_password_correct():
    password = "password123"

    hashed = await hash_password(password)

    result = await verify_password(
        password,
        hashed
    )

    assert result is True


@pytest.mark.asyncio
async def test_verify_password_wrong():
    password = "password123"

    hashed = await hash_password(password)

    result = await verify_password(
        "wrongpassword",
        hashed
    )

    assert result is False

