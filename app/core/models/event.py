from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field

from .location import Location


class Event(Document):
    """Event model."""

    creator_id: PydanticObjectId | None = None
    title: str
    description: str
    category: str
    location: Location
    start_date: datetime
    end_date: datetime
    max_participants: int
    verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """Settings for the Event model."""

        name = "events"
        indexes = [
            "category",
            "location.longitude",
            "location.latitude",
            "start_date",
            "end_date",
            "max_participants",
            "verified",
            "is_active",
        ]
