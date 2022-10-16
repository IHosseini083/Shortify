from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status

from shortify.app import schemas
from shortify.app.api.v1.deps import (
    get_current_active_superuser,
    get_current_active_user,
)
from shortify.app.models import ShortUrl, User
from shortify.app.utils import cbv, paginate

if TYPE_CHECKING:
    from shortify.app.utils.types import PaginationDict

router = APIRouter()


def short_url_not_found(ident_or_slug: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Short URL with identifier/slug {ident_or_slug!r} not found",
    )


@cbv(router)
class BasicUserViews:
    user: User = Depends(get_current_active_user)

    @router.post("/shorten", response_model=schemas.ShortUrl)
    async def shorten_url(self, payload: schemas.ShortUrlCreate) -> ShortUrl:
        if payload.slug and await ShortUrl.get_by_slug(slug=payload.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The URL associated with this slug already exists",
            )
        short_url = await ShortUrl.shorten(
            url=payload.url,
            slug=payload.slug,
            expiration_days=payload.expiration_days,
            user_id=self.user.id,
        )
        return short_url


@cbv(router)
class SuperuserViews:
    superuser: User = Depends(get_current_active_superuser)

    @router.get("/", response_model=schemas.Paginated[schemas.ShortUrl])
    async def get_urls(
        self,
        paging: schemas.PaginationParams = Depends(),
        sorting: schemas.SortingParams = Depends(),
    ) -> "PaginationDict":
        return await paginate(ShortUrl, paging, sorting)

    @router.get("/{ident}", response_model=schemas.ShortUrl)
    async def get_short_url(self, ident: str) -> ShortUrl:
        short_url = await ShortUrl.get_by_ident(ident=ident)
        if not short_url:
            raise short_url_not_found(ident)
        return short_url

    @router.delete("/{ident}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_short_url(self, ident: str) -> None:
        short_url = await ShortUrl.get_by_ident(ident=ident)
        if not short_url:
            raise short_url_not_found(ident)
        await short_url.delete()
