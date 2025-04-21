import re
from datetime import date, datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.config import settings
from app.core.models.user import Gender

PASSWORD_REGEX = re.compile(settings.PASSWORD_PATTERN)


class UserUpdate(BaseModel):
    """Schema for user profile update."""

    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(default=None, min_length=3, max_length=64)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    name: str | None = Field(default=None, min_length=3, max_length=64)
    birth_date: date | None = None
    gender: Gender | None = None
    bio: str | None = None
    interests: list[str] | None = None
    location: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password_format(cls, v: str) -> str:
        """Validate password contains at least one letter and one digit."""
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must contain at least one letter and one digit")
        return v


class UserResponse(BaseModel):
    """Schema for user response."""

    id: PydanticObjectId
    username: str
    email: EmailStr
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

    min_age: int | None = Field(default=None, description="Minimum age")
    max_age: int | None = Field(default=None, description="Maximum age")
    gender: Gender | None = Field(default=None, description="Filter by gender")
    interests: list[str] | None = Field(default=None, description="Filter by interests")
    location: str | None = Field(default=None, description="Filter by location")
    verified: bool | None = Field(default=None, description="Filter by verified status")

    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=100, description="Maximum number of records")
