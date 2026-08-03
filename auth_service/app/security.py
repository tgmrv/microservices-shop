from datetime import datetime, UTC, timedelta

import jwt
from pwdlib import PasswordHash

from .config import settings
from .models import UserORM

password_hash = PasswordHash.recommended()

async def hash_password(password: str) -> str:
    return password_hash.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hash=hashed_password)

async def create_access_token(user: UserORM):
    now = datetime.now(UTC)
    expires_in = now + timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME_SEC)
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": "user",
        "exp": expires_in,
    }

    token = jwt.encode(
        payload,
        key=settings.JWT_SECRET.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )

    return token
