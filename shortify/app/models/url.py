import random
from datetime import datetime, timedelta
from hashlib import md5
from typing import TYPE_CHECKING, List, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

from shortify.app.core.config import settings

if TYPE_CHECKING:
    from shortify.app.schemas import PaginationParams, SortingParams


def generate_ident(url: str, length: int) -> str:
    """Returns a unique identifier for the given URL with the given length."""
    digest = md5(url.encode()).hexdigest()
    return "".join(random.choices(digest, k=length))


class ShortUrl(Document):
    ident: Indexed(str, unique=True)  # type: ignore[valid-type]
    origin: str
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[  # type: ignore[valid-type]
        Indexed(datetime, expireAfterSeconds=0)
    ] = None
    last_visit_at: Optional[datetime] = None
    slug: Optional[Indexed(str, unique=True)] = None  # type: ignore[valid-type]
    user_id: Optional[PydanticObjectId] = None

    @classmethod
    async def shorten(
        cls,
        *,
        url: str,
        slug: Optional[str] = None,
        expiration_days: Optional[float] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> "ShortUrl":
        return await cls(
            ident=generate_ident(url, settings.URL_IDENT_LENGTH),
            origin=url,
            slug=slug,
            expires_at=(
                datetime.utcnow() + timedelta(days=expiration_days)
                if expiration_days
                else None
            ),
            user_id=user_id,
        ).insert()

    @classmethod
    async def get_by_slug(cls, *, slug: str) -> Optional["ShortUrl"]:
        return await cls.find_one(cls.slug == slug)

    @classmethod
    async def get_by_ident(cls, *, ident: str) -> Optional["ShortUrl"]:
        return await cls.find_one(cls.ident == ident)

    @classmethod
    async def get_by_user(
        cls,
        *,
        user_id: PydanticObjectId,
        paging: "PaginationParams",
        sorting: "SortingParams",
    ) -> List["ShortUrl"]:
        return (
            await cls.find(cls.user_id == user_id)
            .skip(paging.skip)
            .limit(paging.limit)
            .sort(
                (sorting.sort, sorting.order.direction),
            )
            .to_list()
        )

    @classmethod
    async def visit(cls, *, instance: "ShortUrl") -> None:
        instance.views += 1
        instance.last_visit_at = datetime.utcnow()
        await instance.save_changes()

    class Settings:
        name = "urls"
        use_state_management = True
