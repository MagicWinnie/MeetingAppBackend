from datetime import date, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.models.user import Gender, PhoneNumberType


class UserUpdate(BaseModel):
    """Schema for user profile update."""

    phone_number: PhoneNumberType | None = None
    email: EmailStr | None = None
    password_hash: str | None = None
    name: str | None = None
    birth_date: date | None = None

    location: str | None = None
    interests: list[str] | None = None

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    """Schema for user response."""

    id: PydanticObjectId
    username: str
    email: str
    name: str | None
    birth_date: date | None
    age: int | None
    gender: Gender | None
    bio: str | None
    interests: list[str]
    location: str | None
    photo_urls: list[str]
    verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseModel):
    """Schema for filtering users."""

    interests: list[str] | None = None
    min_age: int | None = None
    max_age: int | None = None
    location: str | None = None
