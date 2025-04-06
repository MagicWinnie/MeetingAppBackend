from datetime import date, datetime, timezone

from beanie import Document
from pydantic import Field


class User(Document):
    """User model."""

    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    full_name: str | None = None
    birth_date: date | None = None
    location: str | None = None
    interests: list[str] = Field(default_factory=list)

    @property
    def age(self) -> int | None:
        """Calculate age based on birth date."""
        if self.birth_date is None:
            return None
        today = datetime.now(timezone.utc)
        if today.month < self.birth_date.month or (
            today.month == self.birth_date.month and today.day < self.birth_date.day
        ):
            return today.year - self.birth_date.year - 1
        return today.year - self.birth_date.year

    class Settings:
        """Settings for the User model."""

        name = "users"
