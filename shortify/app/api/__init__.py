from fastapi import APIRouter

from shortify.app.api import docs, redirect, v1
from shortify.app.core.config import settings

router = APIRouter(prefix="/api")
router.include_router(v1.router)
router.include_router(docs.router, prefix=f"/{settings.API_V1_STR}/docs")
