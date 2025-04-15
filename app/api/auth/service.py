from datetime import timedelta

import jwt
from beanie.operators import Or
from fastapi import HTTPException, status
from pydantic import EmailStr

from app.api.auth.dependencies import create_token, get_password_hash, verify_password
from app.api.auth.schemas import Token
from app.config import settings
from app.core.models.user import User


class AuthService:
    """Service for authentication."""

    @staticmethod
    async def register(name: str, username: str, email: EmailStr, password: str) -> User:
        """Register a new user.

        Args:
            name: User's name
            username: User's username
            email: User's email
            password: User's password

        Returns:
            Newly created user object

        Raises:
            HTTPException (400): If user with this username or email already exists
        """
        existing_user = await User.find_one(Or(User.username == username, User.email == email))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists",
            )

        hashed_password = get_password_hash(password)
        user = User(name=name, username=username, email=email, password_hash=hashed_password)
        await user.insert()
        return user

    @staticmethod
    async def login(username: str, password: str) -> Token:
        """Authenticate a user and generate access and refresh tokens.

        Args:
            username: User's username
            password: User's password

        Returns:
            Object containing access and refresh tokens

        Raises:
            HTTPException (401): If credentials are invalid
        """
        user = await User.find_one(User.username == username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        refresh_token = create_token(
            subject=str(user.id),
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def refresh_token(refresh_token: str) -> Token:
        """Generate new access and refresh tokens using a valid refresh token.

        Args:
            refresh_token: Current refresh token

        Returns:
            Object containing new access and refresh tokens

        Raises:
            HTTPException (401): If refresh token is invalid or user not found
        """
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user = await User.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token = create_token(
                subject=str(user.id),
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )

            new_refresh_token = create_token(
                subject=str(user.id),
                expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )

            return Token(access_token=access_token, refresh_token=new_refresh_token)
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
