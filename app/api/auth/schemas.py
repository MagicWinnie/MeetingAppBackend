import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.config import settings

PASSWORD_REGEX = re.compile(settings.PASSWORD_PATTERN)


class UserCreate(BaseModel):
    """User creation schema."""

    name: str = Field(..., min_length=3, max_length=64)
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_format(cls, v: str) -> str:
        """Validate password contains at least one letter and one digit."""
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must contain at least one letter and one digit")
        return v


class UserLogin(BaseModel):
    """User login schema."""

    username: str
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


class EmailVerification(BaseModel):
    """Email verification schema."""

    otp: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema."""

    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_format(cls, v: str) -> str:
        """Validate password contains at least one letter and one digit."""
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must contain at least one letter and one digit")
        return v
