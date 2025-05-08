from pydantic import BaseModel


class Location(BaseModel):
    """Location model."""

    latitude: float
    longitude: float
