from typing import Optional, cast

from beanie import PydanticObjectId
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyQuery, OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from shortify.app import schemas
from shortify.app.core import security
from shortify.app.core.config import settings
from shortify.app.models import User

bearer_token = OAuth2PasswordBearer(
    tokenUrl=f"/api/{settings.API_V1_STR}/auth/access-token",
    auto_error=False,
)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)


async def authenticate_bearer_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        data = schemas.AuthTokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
    else:
        return await User.get(cast(PydanticObjectId, data.sub))


async def get_current_user(
    api_key: Optional[str] = Depends(api_key_query),
    token: Optional[str] = Depends(bearer_token),
) -> User:
    """Gets the current user from the database."""
    if api_key:  # API Key has priority over Bearer token
        user = await User.get_by_api_key(api_key=api_key)
    elif token:
        user = await authenticate_bearer_token(token)
    else:
        # This is the exception that is raised by the Depends() call
        # when the user is not authenticated and auto_error is True.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )
    if not user:
        if api_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Gets the current active user from the database."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Gets the current active superuser from the database."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
