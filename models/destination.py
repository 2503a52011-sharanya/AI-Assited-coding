from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Destination:
    id: int
    name: str
    state: str
    country: str = "India"
    city: Optional[str] = None
    latitude: float = 0.0
    longitude: float = 0.0
    description: str = ""
    best_season: str = "All year"
    ideal_duration_days: int = 3
    avg_daily_budget: float = 3500.0
    tags: str = ""
    image_url: str = ""
    is_popular: bool = False


@dataclass
class Attraction:
    id: int
    destination_id: int
    name: str
    category: str
    description: str = ""
    entry_fee: float = 0.0
    opening_time: str = "09:00"
    closing_time: str = "18:00"
    avg_visit_duration_hours: float = 2.0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_indoor: bool = False
    rating: float = 4.5


@dataclass
class Hotel:
    id: int
    destination_id: int
    name: str
    hotel_type: str = "Budget hotel"
    star_rating: int = 3
    address: str = ""
    price_per_night: float = 2000.0
    amenities: str = ""
    rating: float = 4.2
    image_url: str = ""


@dataclass
class Activity:
    id: int
    destination_id: int
    title: str
    category: str
    description: str
    price_per_person: float
    duration_hours: float = 2.0
    suitable_for: str = "All"
    rating: float = 4.7
