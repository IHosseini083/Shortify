from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from shortify.app import api
from shortify.app.core.config import settings
from shortify.app.db import init_db

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Fast and reliable URL shortener powered by FastAPI and MongoDB.",
    # Set current documentation page to v1
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
    redoc_url=None,  # disable ReDoc documentation
)

# Add the router responsible for all /api/ endpoint requests
app.include_router(api.router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize services on startup."""
    await init_db.init()


# Custom HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc: StarletteHTTPException) -> JSONResponse:
    errors = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        406: "NOT_ACCEPTABLE",
        409: "CONFLICT",
        500: "INTERNAL_SERVER_ERROR",
    }
    return JSONResponse(
        content={
            "status": errors.get(exc.status_code, f"ERROR_{exc.status_code}"),
            "message": exc.detail,
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )
