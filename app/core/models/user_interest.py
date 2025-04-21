from beanie import Document


class UserInterest(Document):
    """User interest model."""

    category: str
    name: str

    class Settings:
        """Settings for the user interest model."""

        name = "user_interests"
        indexes = ["category", "name"]
