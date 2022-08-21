from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from shortify.app.core.config import settings
from shortify.app.models import gather_documents


async def init() -> None:
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(
        database=client.shortify,
        document_models=gather_documents(),  # type: ignore[arg-type]
    )
