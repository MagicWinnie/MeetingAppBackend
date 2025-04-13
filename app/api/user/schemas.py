from datetime import date, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.models.user import PhoneNumberType


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
    phone_number: PhoneNumberType
    email: EmailStr | None = None
    name: str | None = None
    birth_date: date | None = None
    age: int | None = None
    location: str | None = None
    photo_urls: list[str] | None = None
    interests: list[str]
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseModel):
    """Schema for filtering users."""

    interests: list[str] | None = None
    min_age: int | None = None
    max_age: int | None = None
    location: str | None = None
