import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.core.models import MODELS

logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize the database."""
    client = AsyncIOMotorClient(
        settings.MONGO_URI,
        connectTimeoutMS=5000,
        timeoutms=5000,
    )
    await init_beanie(client[settings.MONGO_DB], document_models=MODELS)
    logger.info("Database initialized")
