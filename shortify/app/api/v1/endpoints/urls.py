from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from shortify.app import schemas
from shortify.app.api.v1.deps import (
    get_current_active_superuser,
    get_current_active_user,
)
from shortify.app.models import ShortUrl, User

router = APIRouter()


@router.get("/", response_model=List[schemas.ShortUrl])
async def get_urls(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    _=Depends(get_current_active_superuser),
) -> List[ShortUrl]:
    return await ShortUrl.find_all(skip, limit).to_list()


@router.get("/{ident}", response_model=schemas.ShortUrl)
async def get_short_url(
    ident: str,
    _=Depends(get_current_active_superuser),
) -> ShortUrl:
    short_url = await ShortUrl.get_by_ident(ident=ident)
    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Short URL with ID {ident!r} does not exist",
        )
    return short_url


@router.post("/shorten", response_model=schemas.ShortUrl)
async def shorten_url(
    payload: schemas.ShortUrlCreate,
    user: User = Depends(get_current_active_user),
) -> ShortUrl:
    if payload.slug and await ShortUrl.get_by_slug(slug=payload.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The URL associated with this slug already exists.",
        )
    if not (short_url := await ShortUrl.get_by_origin(origin=payload.url)):
        short_url = await ShortUrl.shorten(
            url=payload.url,
            slug=payload.slug,
            expiration_days=payload.expiration_days,
            user_id=user.id,
        )
    return short_url
