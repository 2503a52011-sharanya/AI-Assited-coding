from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class BookingItem:
    passenger_name: str
    passenger_age: int
    seat_or_room: Optional[str] = None


@dataclass
class Booking:
    id: Optional[int]
    user_id: int
    booking_reference: str
    category: str # Flight, Train, Bus, Hotel, Cab, Activity
    provider_name: str
    item_title: str
    travel_date: str
    passenger_count: int
    total_amount: float
    status: str = "Confirmed"
    is_demo: bool = True
    items: List[BookingItem] = field(default_factory=list)
