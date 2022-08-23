from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from shortify.app import models, schemas
from shortify.app.core import security
from shortify.app.core.config import settings

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized, invalid credentials or access token",
        },
    },
)


@router.post(
    "/access-token",
    response_model=schemas.AuthToken,
    description="Retrieve an access token for the given username and password.",
)
async def generate_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, str]:
    """Get an access token for future requests."""
    user = await models.User.authenticate(
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    expires_in = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id,
            expires_delta=expires_in,
        ),
        "token_type": "bearer",
    }
