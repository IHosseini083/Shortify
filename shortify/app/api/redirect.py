from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import RedirectResponse

from shortify.app.api.v1.endpoints.urls import short_url_not_found
from shortify.app.models import ShortUrl

router = APIRouter(
    # Hide this router from the OpenAPI docs since it's not a part of
    # the API, but rather a part of the main app.
    include_in_schema=False,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
        },
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "description": "Successfully redirected to the original URL",
        },
    },
)


@router.get("/{ident}", response_class=RedirectResponse)
async def redirect_by_identifier(worker: BackgroundTasks, ident: str) -> str:
    if short_url := await ShortUrl.get_by_ident(ident=ident):
        worker.add_task(ShortUrl.visit, instance=short_url)
        return short_url.origin
    raise short_url_not_found(ident)
