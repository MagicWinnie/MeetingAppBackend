from datetime import date, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr


class UserUpdate(BaseModel):
    """Schema for user profile update."""

    email: EmailStr | None = None
    full_name: str | None = None
    birth_date: date | None = None
    location: str | None = None
    interests: list[str] | None = None

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    """Schema for user response."""

    id: PydanticObjectId
    email: EmailStr
    full_name: str | None = None
    birth_date: date | None = None
    age: int | None = None
    location: str | None = None
    interests: list[str]
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseModel):
    """Schema for filtering users."""

    interests: list[str] | None = None
    min_age: int | None = None
    max_age: int | None = None
    location: str | None = None
