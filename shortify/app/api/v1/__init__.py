from fastapi import APIRouter

from shortify.app.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
