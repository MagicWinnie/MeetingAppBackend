from datetime import date, datetime, timezone


def get_age(birth_date: date) -> int:
    """Get age from birth date."""
    today = datetime.now(timezone.utc)
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        return today.year - birth_date.year - 1
    return today.year - birth_date.year
