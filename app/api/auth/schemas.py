from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """User creation schema."""

    name: str
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)


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
