from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from shortify.app.core.config import settings

router = APIRouter()


@router.get("/", include_in_schema=False)
async def get_docs() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} | Docs {settings.API_V1_STR}",
        swagger_favicon_url="/static/img/favicon.png",
    )
