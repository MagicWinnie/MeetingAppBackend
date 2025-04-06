import logging
import tomllib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

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
    yield
    logger.info("Stopping FastAPI app")


app = FastAPI(
    title=pyproject_data["project"]["name"],
    description=pyproject_data["project"]["description"],
    version=pyproject_data["project"]["version"],
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
