import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

from .models import MODELS

logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize the database."""
    client = AsyncIOMotorClient(
        settings.MONGO_URI,
        connectTimeoutMS=settings.MONGO_TIMEOUT,
        timeoutMS=settings.MONGO_TIMEOUT,
    )
    await init_beanie(client[settings.MONGO_DB], document_models=MODELS)
    logger.info("Database initialized")
