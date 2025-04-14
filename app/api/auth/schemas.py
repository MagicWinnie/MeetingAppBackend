from pydantic import BaseModel, Field

from app.core.models.user import PhoneNumberType


class UserCreate(BaseModel):
    """User creation schema."""

    name: str
    phone_number: PhoneNumberType
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema."""

    phone_number: PhoneNumberType
    password: str


class Token(BaseModel):
    """Token schema."""

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str
    exp: int


class TokenRefresh(BaseModel):
    """Token refresh schema."""

    refresh_token: str
