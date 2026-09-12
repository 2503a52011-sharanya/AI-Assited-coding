from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class User:
    id: int
    name: str
    email: str
    role: str = "user"
    phone: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class UserPreferences:
    user_id: int
    travel_style: str = "Comfortable"
    preferred_budget_range: str = "₹10,000 - ₹25,000"
    preferred_transport: str = "Train"
    preferred_accommodation: str = "Budget hotel"
    food_preference: str = "Local food"
    interests: List[str] = field(default_factory=list)
    accessibility_requirements: str = ""
