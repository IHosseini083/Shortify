import random
from datetime import datetime
from hashlib import md5
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field

from shortify.app.core.config import settings


def generate_ident(url: str, length: int) -> str:
    """Returns a unique identifier for the given URL with the given length."""
    digest = md5(url.encode()).hexdigest()
    return "".join(random.choices(digest, k=length))


class ShortUrl(Document):
    ident: Indexed(str, unique=True)  # type: ignore[valid-type]
    origin: str
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO: Add a TLL index for document expiration
    slug: Optional[Indexed(str, unique=True)] = None  # type: ignore[valid-type]

    @classmethod
    async def shorten(cls, *, url: str, slug: Optional[str] = None) -> "ShortUrl":
        return await cls(
            ident=generate_ident(url, settings.URL_IDENT_LENGTH),
            origin=url,
            slug=slug,
        ).insert()

    @classmethod
    async def get_by_slug(cls, *, slug: str) -> Optional["ShortUrl"]:
        return await cls.find_one(cls.slug == slug)

    @classmethod
    async def get_by_ident(cls, *, ident: str) -> Optional["ShortUrl"]:
        return await cls.find_one(cls.ident == ident)

    class Settings:
        name = "urls"
        use_state_management = True
