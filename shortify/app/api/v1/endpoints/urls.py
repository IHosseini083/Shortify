from fastapi import APIRouter, Depends, HTTPException, status

from shortify.app import schemas
from shortify.app.api.v1.deps import get_current_active_superuser
from shortify.app.models import ShortUrl, User

router = APIRouter()


@router.post("/shorten", response_model=schemas.ShortUrl)
async def shorten_url(
    payload: schemas.ShortUrlCreate,
    current_user: User = Depends(get_current_active_superuser),
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
            user_id=current_user.id,
        )
    return short_url
