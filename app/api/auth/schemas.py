from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.config import settings


class UserCreate(BaseModel):
    """User creation schema."""

    model_config = ConfigDict(regex_engine="python-re")

    name: str = Field(..., min_length=3, max_length=64)
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        pattern=settings.PASSWORD_REGEX,
        description="Password must contain at least one letter and one digit, and be at least 8 characters long",
    )


class UserLogin(BaseModel):
    """User login schema."""

    model_config = ConfigDict(regex_engine="python-re")

    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(
        ...,
        min_length=8,
        pattern=settings.PASSWORD_REGEX,
        description="Password must contain at least one letter and one digit, and be at least 8 characters long",
    )


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
