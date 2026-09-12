from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ItineraryItem:
    day_number: int
    time_slot: str
    activity_title: str
    activity_type: str # Sightseeing, Food, Transit, Leisure, Check-in
    location_name: str = ""
    estimated_cost: float = 0.0
    notes: str = ""


@dataclass
class Trip:
    id: Optional[int]
    user_id: int
    trip_name: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    days: int
    travelers_count: int
    traveler_type: str
    travel_style: str
    allocated_budget: float
    total_estimated_cost: float
    status: str = "Planned"
    itinerary_items: List[ItineraryItem] = field(default_factory=list)


@dataclass
class TripBudget:
    transport_cost: float
    accommodation_cost: float
    food_cost: float
    activities_cost: float
    local_transport_cost: float
    buffer_cost: float
    total_cost: float
    is_optimized: bool = False
    savings_achieved: float = 0.0
