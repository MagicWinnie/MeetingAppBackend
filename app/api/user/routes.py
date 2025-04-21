from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.api.auth.dependencies import get_current_user
from app.core.models.user import User

from .schemas import UserFilter, UserResponse, UserUpdate
from .service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """Get the profile of the current authenticated user.

    Returns status code 401 if token is invalid or user doesn't exist.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Update the profile of the current authenticated user.

    Returns status code 401 if token is invalid or user doesn't exist.
    Returns status code 400 if username or email already exists.
    """
    return await UserService.update_user(current_user, user_update)


@router.get("/", response_model=list[UserResponse])
async def find_users(
    current_user: Annotated[User, Depends(get_current_user)],
    filter_params: Annotated[UserFilter, Query(..., description="Filter parameters")],
):
    """Search users with filters."""
    return await UserService.search_users(
        filter_params=filter_params,
        current_user_id=current_user.id,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str, _: Annotated[User, Depends(get_current_user)]):
    """Get the profile of another user by ID.

    Returns status code 404 if user is not found.
    """
    return await UserService.get_user_by_id(user_id)


@router.post("/me/picture", response_model=UserResponse)
async def upload_profile_picture(
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    """Upload a profile picture to AWS S3."""
    return await UserService.upload_profile_picture(current_user, file)
