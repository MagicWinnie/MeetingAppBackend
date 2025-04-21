from fastapi import APIRouter

from .schemas import UserInterestsResponse
from .service import UserInterestService

router = APIRouter(prefix="/user-interests", tags=["User Interests"])


@router.get("/", response_model=UserInterestsResponse)
async def get_all_user_interests():
    """Get all user interests."""
    return await UserInterestService.get_all_user_interests()


@router.get("/{category}", response_model=list[str])
async def get_user_interests(category: str):
    """Get user interests by category."""
    return await UserInterestService.get_user_interests(category)
