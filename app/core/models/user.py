from datetime import date, datetime, timezone
from enum import Enum
from typing import Annotated

from beanie import Document
from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

# Currently not used, but let it be here for future use
PhoneNumberType = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(number_format="E164"),
]


class Gender(str, Enum):
    """Gender enum."""

    MALE = "male"
    FEMALE = "female"


class User(Document):
    """User model."""

    username: str
    email: str
    password_hash: str
    name: str | None = None
    birth_date: date | None = None
    gender: Gender | None = None
    bio: str | None = None
    interests: list[str] = Field(default_factory=list)
    location: str | None = None
    photo_urls: list[str] = Field(default_factory=list)
    verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
