import logging
import tomllib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ROUTERS
from app.core.database import initialize_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

logger = logging.getLogger(__name__)


with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan for the FastAPI app."""
    logger.info("Starting FastAPI app")
    await initialize_database()
    yield
    logger.info("Stopping FastAPI app")


app = FastAPI(
    title=pyproject_data["project"]["name"],
    description=pyproject_data["project"]["description"],
    version=pyproject_data["project"]["version"],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ROUTERS:
    app.include_router(router)
