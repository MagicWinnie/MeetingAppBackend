import secrets
import string


def generate_otp(length: int = 6) -> str:
    """Generate a random OTP code.

    Args:
        length: Length of the OTP (default is 6 digits)

    Returns:
        Random string of digits
    """
    return "".join(secrets.choice(string.digits) for _ in range(length))
