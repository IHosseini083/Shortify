from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed, Link
from pydantic import EmailStr
from pydantic.fields import Field

from shortify.app.core.security import verify_password
from shortify.app.models.url import ShortUrl


class User(Document):
    username: Indexed(str, unique=True)  # type: ignore[valid-type]
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    urls: List[Link[ShortUrl]] = Field(default_factory=list)

    @classmethod
    async def get_by_username(cls, *, username: str) -> Optional["User"]:
        return await cls.find_one(cls.username == username)

    @classmethod
    async def authenticate(
        cls,
        *,
        username: str,
        password: str,
    ) -> Optional["User"]:
        user = await cls.find_one(cls.username == username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    class Settings:
        name = "users"
        use_state_management = True
