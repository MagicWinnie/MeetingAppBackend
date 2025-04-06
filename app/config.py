from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the project."""

    # MongoDB credentials
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "db"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "MeetingApp"

    @property
    def MONGO_URI(self) -> str:
        """Construct MongoDB URI from credentials."""
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/?authSource=admin"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
