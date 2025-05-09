from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.models.user import User

from .dependencies import get_current_user
from .schemas import EmailVerification, Token, TokenRefresh, UserCreate
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user.

    Returns status code 400, if username or email already exists.
    """
    await AuthService.register(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )
    return await AuthService.login(username=user_data.username, password=user_data.password)


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate and get access token.

    Returns status code 401, if authentication fails.
    """
    return await AuthService.login(username=form_data.username, password=form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh: TokenRefresh):
    """Refresh access token.

    Returns status code 401, if refresh token is invalid.
    """
    return await AuthService.refresh_token(refresh_token=refresh.refresh_token)


@router.post("/verify-email", response_model=None)
async def verify_email(verification: EmailVerification, current_user: Annotated[User, Depends(get_current_user)]):
    """Verify user email with OTP.

    Returns status code 400, if OTP is invalid or expired.
    Returns status code 404, if user is not found.
    """
    await AuthService.verify_email(user_id=str(current_user.id), otp=verification.otp)


@router.post("/resend-verification", response_model=None)
async def resend_verification(current_user: Annotated[User, Depends(get_current_user)]):
    """Resend verification email with new OTP.

    Returns status code 400, if user is already verified.
    Returns status code 404, if user is not found.
    """
    await AuthService.resend_verification_email(user_id=str(current_user.id))
