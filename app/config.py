from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the project."""

    # MongoDB credentials
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "db"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "MeetingApp"
    MONGO_TIMEOUT: int = 5000

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AWS S3 settings
    AWS_S3_BUCKET: str = "meetingapp-profile-pictures"
    AWS_S3_REGION: str = "us-east-1"
    AWS_S3_ENDPOINT_URL: str = "http://185.157.214.169:4566"
    AWS_S3_ACCESS_KEY_ID: str
    AWS_S3_SECRET_ACCESS_KEY: str

    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str

    # Email settings
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_FROM: str
    EMAIL_PASSWORD: str
    EMAIL_TIMEOUT: int = 3

    PASSWORD_PATTERN: str = r"^(?=.*[a-zA-Z])(?=.*\d).+$"

    @property
    def MONGO_URI(self) -> str:
        """Construct MongoDB URI from credentials."""
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/?authSource=admin"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
