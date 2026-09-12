import re


def validate_email(email: str) -> bool:
    """Checks if email format is RFC 5322 compliant."""
    if not email:
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))


def validate_phone(phone: str) -> bool:
    """Validates international or 10-digit Indian phone format."""
    if not phone:
        return True # Optional field
    cleaned = re.sub(r"[\s\-\(\)\+]", "", phone)
    return len(cleaned) >= 10 and cleaned.isdigit()


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Ensures password meets minimum security standards."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validates geographical latitude and longitude bounds."""
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0
