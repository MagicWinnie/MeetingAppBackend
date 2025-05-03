from datetime import date, datetime, timezone
from enum import Enum
from typing import Annotated

from beanie import Document
from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

from app.core.utils.age import get_age

from .location import Location

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
    location: Location | None = None
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
        return get_age(self.birth_date)

    class Settings:
        """Settings for the User model."""

        name = "users"
        indexes = [
            "username",
            "email",
            "birth_date",
            "gender",
            "location.longitude",
            "location.latitude",
            "verified",
            "is_active",
        ]
