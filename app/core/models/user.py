from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class User(Document):
    """User model."""

    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """Settings for the User model."""

        name = "users"
