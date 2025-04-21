from pydantic import BaseModel


class UserInterestsResponse(BaseModel):
    """User interests response."""

    interests: dict[str, list[str]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "interests": {
                        "Хобби": ["Компьютерные игры", "Психология", "..."],
                        "Социальная жизнь": ["Кинотеатры", "Концерты и шоу", "..."],
                    },
                },
            ],
        },
    }
