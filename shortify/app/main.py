from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from shortify.app import api
from shortify.app.core.config import settings
from shortify.app.core.logging import setup_logging
from shortify.app.db import init_db
from shortify.app.schemas.validation_error import APIValidationError

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Get authentication token",
    },
    {
        "name": "Users",
        "description": "User registration and management",
    },
    {
        "name": "URLs",
        "description": "Shorten and manage URLs",
    },
]

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Fast and reliable URL shortener powered by FastAPI and MongoDB.",
    # Set current documentation specs to v1
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
    docs_url=None,
    redoc_url=None,
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable Entity (Validation Error)",
            "model": APIValidationError,  # This will add OpenAPI schema to the docs
        },
    },
)

app.mount("/static", StaticFiles(directory="shortify/app/static"), name="static")

# Add the router responsible for all /api/ endpoint requests
app.include_router(api.router)
# Include redirection router in the main app
app.include_router(api.redirect.router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.USE_CORRELATION_ID:
    from shortify.app.middlewares.correlation import CorrelationMiddleware

    app.add_middleware(CorrelationMiddleware)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize services on startup."""
    setup_logging()
    await init_db.init()


# Custom HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc: StarletteHTTPException) -> ORJSONResponse:
    return ORJSONResponse(
        content={
            "message": exc.detail,
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(
    _,
    exc: RequestValidationError,
) -> ORJSONResponse:
    return ORJSONResponse(
        content=APIValidationError.from_pydantic(exc).dict(exclude_none=True),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
