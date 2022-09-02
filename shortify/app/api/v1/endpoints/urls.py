from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from shortify.app import schemas
from shortify.app.api.v1.deps import (
    get_current_active_superuser,
    get_current_active_user,
)
from shortify.app.models import ShortUrl, User

router = APIRouter()


def short_url_not_found(ident: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Short URL with identifier {ident!r} not found.",
    )


@router.get("/", response_model=schemas.Paginated[schemas.ShortUrl])
async def get_urls(
    params: schemas.PaginationParams = Depends(),
    _=Depends(get_current_active_superuser),
) -> Dict[str, Any]:
    results = await ShortUrl.find().skip(params.skip).limit(params.limit).to_list()
    return {
        "page": params.page,
        "per_page": params.per_page,
        "total": await ShortUrl.count(),
        "results": results,
    }


@router.get("/{ident}", response_model=schemas.ShortUrl)
async def get_short_url(
    ident: str,
    _=Depends(get_current_active_superuser),
) -> ShortUrl:
    short_url = await ShortUrl.get_by_ident(ident=ident)
    if not short_url:
        raise short_url_not_found(ident=ident)
    return short_url


@router.delete("/{ident}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_short_url(
    ident: str,
    _=Depends(get_current_active_superuser),
) -> None:
    short_url = await ShortUrl.get_by_ident(ident=ident)
    if not short_url:
        raise short_url_not_found(ident=ident)
    await short_url.delete()


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
    short_url = await ShortUrl.shorten(
        url=payload.url,
        slug=payload.slug,
        expiration_days=payload.expiration_days,
        user_id=user.id,
    )
    return short_url
