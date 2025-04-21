import asyncio
import os

import anyio

from app.core.database import initialize_database
from app.core.models import UserInterest

PWD = os.path.dirname(os.path.abspath(__file__))


async def main():
    """Imports user interests from file."""
    await initialize_database()

    async with await anyio.open_file(os.path.join(PWD, "interests.txt"), "r", encoding="utf-8") as f:
        interests = await f.readlines()
        interests = list(map(str.strip, interests))

    to_create = []
    category = ""
    for interest in interests:
        if interest.endswith(":"):
            category = interest.rstrip(":")
        elif interest:
            if not category:
                raise ValueError("Category is not set")
            to_create.append(UserInterest(category=category, name=interest))

    if not to_create:
        raise ValueError("No interests to create")

    print(f"Creating {len(to_create)} interests")

    await UserInterest.delete_all()
    await UserInterest.insert_many(to_create)


if __name__ == "__main__":
    asyncio.run(main())
