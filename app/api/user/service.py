import uuid
from datetime import date, datetime, timedelta, timezone

import boto3
from beanie import PydanticObjectId
from beanie.operators import GTE, LTE, And, In
from botocore.config import Config as BotoConfig
from fastapi import HTTPException, UploadFile, status

from app.api.user.schemas import UserFilter, UserUpdate
from app.config import settings
from app.core.models.user import User

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
    config=BotoConfig(
        retries={
            "max_attempts": 3,
            "mode": "standard",
        },
        connect_timeout=5,
        read_timeout=10,
        region_name=settings.AWS_S3_REGION,
    ),
)


class UserService:
    """Service for users."""

    @staticmethod
    async def get_user_by_id(user_id: str) -> User:
        """Get a user by ID.

        Args:
            user_id: User ID to find

        Returns:
            User object

        Raises:
            HTTPException (404): If user not found
        """
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    @staticmethod
    async def update_user(current_user: User, user_update: UserUpdate) -> User:
        """Update a user profile.

        Args:
            current_user: User to update
            user_update: Update data

        Returns:
            Updated user

        Raises:
            HTTPException (400): If phone number already exists
        """
        update_data = user_update.model_dump(exclude_unset=True)

        if "phone_number" in update_data:
            user = await User.find_one(User.phone_number == update_data["phone_number"])
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already exists",
                )

        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            await current_user.update({"$set": update_data})

        return current_user

    @staticmethod
    async def search_users(
        filter_params: UserFilter,
        skip: int = 0,
        limit: int = 100,
        current_user_id: PydanticObjectId | None = None,
    ) -> list[User]:
        """Search users with filters.

        Args:
            filter_params: Filter criteria
            skip: Number of records to skip
            limit: Maximum number of records to return
            current_user_id: Current user ID to exclude from results

        Returns:
            List of users matching criteria
        """
        query_conditions = []

        if filter_params.interests is not None:
            query_conditions.append(In(User.interests, filter_params.interests))

        today = date.today()

        if filter_params.min_age is not None:
            max_birth_date = date(today.year - filter_params.min_age, today.month, today.day)
            query_conditions.append(LTE(User.birth_date, max_birth_date))

        if filter_params.max_age is not None:
            min_birth_date = date(today.year - filter_params.max_age - 1, today.month, today.day) + timedelta(days=1)
            query_conditions.append(GTE(User.birth_date, min_birth_date))

        if filter_params.location is not None:
            query_conditions.append(User.location == filter_params.location)

        query = And(*query_conditions) if query_conditions else {}

        users_query = User.find(query)

        if current_user_id is not None:
            users_query = users_query.find(User.id != current_user_id)

        return await users_query.skip(skip).limit(limit).to_list()

    @staticmethod
    async def upload_profile_picture(current_user: User, file: UploadFile) -> User:
        """Upload a profile picture to AWS S3 and update the user's photo_urls."""
        if not file.filename or not file.filename.endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must have a valid filename and extension",
            )
        unique_filename = f"{current_user.id}_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        file.file.seek(0)
        s3_client.upload_fileobj(file.file, settings.AWS_S3_BUCKET, unique_filename)
        file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_S3_BUCKET}/{unique_filename}"
        current_user.photo_urls.append(file_url)
        await current_user.update({"$set": {"photo_urls": current_user.photo_urls}})
        return current_user
