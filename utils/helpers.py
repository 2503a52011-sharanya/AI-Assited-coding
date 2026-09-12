import math
import random
import string
from datetime import datetime


def format_currency(amount: float, symbol: str = "₹") -> str:
    """Formats float number into Indian currency representation with comma formatting."""
    try:
        val = int(round(amount))
        s = str(abs(val))
        if len(s) <= 3:
            formatted = s
        else:
            last3 = s[-3:]
            remaining = s[:-3]
            groups = []
            while len(remaining) > 2:
                groups.append(remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                groups.append(remaining)
            groups.reverse()
            formatted = ",".join(groups) + "," + last3
        return f"{'-' if val < 0 else ''}{symbol}{formatted}"
    except Exception:
        return f"{symbol}{amount:,.2f}"


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points in kilometers."""
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


def generate_reference_id(prefix: str = "BK") -> str:
    """Generates unique, realistic booking or trip reference ID."""
    timestamp = datetime.now().strftime("%y%m%d")
    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{timestamp}-{random_str}"
