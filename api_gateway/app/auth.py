import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from .config import settings
from .schemas import CurrentUserSchema


def decode_access_token(
    token: str,
) -> CurrentUserSchema:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM]
        )
        return CurrentUserSchema(id=payload["user_id"], email=payload["email"])
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())
) -> CurrentUserSchema:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return decode_access_token(credentials.credentials)