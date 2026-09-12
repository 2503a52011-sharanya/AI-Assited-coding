import pytest
from services.itinerary_service import ItineraryService


def test_itinerary_generation():
    attractions = [
        {"name": "Borra Caves", "category": "Nature", "entry_fee": 80.0, "duration_hours": 2.0},
        {"name": "Katiki Waterfalls", "category": "Nature", "entry_fee": 20.0, "duration_hours": 2.5},
        {"name": "Tribal Museum", "category": "Culture", "entry_fee": 40.0, "duration_hours": 1.5}
    ]
    activities = [
        {"title": "Dhimsa Tribal Dance", "category": "Culture", "price_per_person": 200.0, "duration_hours": 1.5, "description": "Dance"}
    ]

    itinerary = ItineraryService.generate_itinerary(
        destination_name="Araku Valley",
        days=3,
        traveler_type="Couple",
        interests=["Nature", "Photography"],
        attractions=attractions,
        activities=activities,
        hotel_name="Haritha Resort"
    )

    assert len(itinerary) > 0
    days_in_schedule = set(i["day"] for i in itinerary)
    assert days_in_schedule == {1, 2, 3}

    # Verify check-in exists on Day 1
    day1_titles = [i["activity_title"] for i in itinerary if i["day"] == 1]
    assert any("Check-in" in t for t in day1_titles)

    # Verify meals exist
    day2_types = [i["activity_type"] for i in itinerary if i["day"] == 2]
    assert "Food" in day2_types
