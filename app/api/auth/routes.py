from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.schemas import Token, UserCreate
from app.api.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=None)
async def register(user_data: UserCreate):
    """Register a new user.

    Returns status code 400, if email already exists.
    """
    await AuthService.register(email=user_data.email, password=user_data.password)


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Log in and get access token.

    Returns status code 401, if email or password is incorrect.
    """
    return await AuthService.login(email=form_data.username, password=form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token.

    Returns status code 401, if refresh token is invalid.
    """
    return await AuthService.refresh_token(refresh_token=refresh_token)
