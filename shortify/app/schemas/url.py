from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, validator


class ShortUrlCreate(BaseModel):
    url: AnyUrl
    slug: Optional[str] = Field(None, max_length=64, min_length=3)
    expiration_days: Optional[float] = Field(None, ge=0.0)

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
    expires_at: Optional[datetime] = None
    last_visit_at: Optional[datetime] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True
