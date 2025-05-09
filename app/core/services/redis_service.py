import redis

from app.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


class RedisService:
    """Service for Redis operations."""

    @staticmethod
    async def store_otp(user_id: str, otp: str, expiry_seconds: int = 600) -> bool:
        """Store OTP in Redis with expiration.

        Args:
            user_id: User's ID
            otp: One-time password
            expiry_seconds: Time in seconds until OTP expires (default 10 minutes)

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            key = f"otp:{user_id}"
            redis_client.set(key, otp, ex=expiry_seconds)
            return True
        except Exception:
            return False

    @staticmethod
    async def get_otp(user_id: str) -> str | None:
        """Get OTP from Redis.

        Args:
            user_id: User's ID

        Returns:
            OTP if found and not expired, None otherwise
        """
        try:
            key = f"otp:{user_id}"
            value = redis_client.get(key)
            if value is None:
                return None
            return str(value)
        except Exception:
            return None

    @staticmethod
    async def delete_otp(user_id: str) -> bool:
        """Delete OTP from Redis.

        Args:
            user_id: User's ID

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            key = f"otp:{user_id}"
            redis_client.delete(key)
            return True
        except Exception:
            return False
