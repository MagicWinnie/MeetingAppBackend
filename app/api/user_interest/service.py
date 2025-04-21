from app.core.models import UserInterest

from .schemas import UserInterestsResponse


class UserInterestService:
    """Service for user interests."""

    @staticmethod
    async def get_all_user_interests() -> UserInterestsResponse:
        """Get all user interests.

        Returns:
            List of user interests in a dictionary format.
        """
        interests = {}
        async for interest in UserInterest.find_all():
            if interest.category not in interests:
                interests[interest.category] = []
            interests[interest.category].append(interest.name)

        return UserInterestsResponse(interests=interests)

    @staticmethod
    async def get_user_interests(category: str) -> list[str]:
        """Get user interests by category.

        Returns:
            List of user interests.
        """
        return [interest.name async for interest in UserInterest.find(UserInterest.category == category)]
