from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, validator


class ShortUrlCreate(BaseModel):
    url: AnyUrl
    slug: Optional[str] = Field(None, max_length=64, min_length=3)

    @validator("slug")
    def slug_normalizer(cls, slug: Optional[str]) -> Optional[str]:  # noqa
        if slug:
            slug = slug.strip().lower().replace(" ", "-")
        return slug


class ShortUrl(BaseModel):
    ident: str
    origin: AnyUrl
    views: int
    created_at: datetime
    slug: Optional[str] = None

    class Config:
        orm_mode = True
