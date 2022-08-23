from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class AuthTokenPayload(BaseModel):
    sub: Optional[PydanticObjectId] = None


class AuthToken(BaseModel):
    access_token: str
    token_type: str
