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
            detail="The URL associated with this slug already exists",
        )
    short_url = await ShortUrl.shorten(url=payload.url, slug=payload.slug)
    current_user.urls.append(short_url)  # type: ignore[arg-type]
    # Because we already save the short URL to db, we don't need to
    # set the 'link_rule' to 'WriteRules.WRITE'
    await current_user.save()
    return short_url
