import pytest
from services.destination_service import DestinationService
from services.weather_service import WeatherService
from services.train_service import TrainService
from services.hotel_service import HotelService
from services.activity_service import ActivityService
from services.itinerary_service import ItineraryService
from services.budget_service import BudgetService
from services.booking_service import BookingService
from database.queries import save_trip, save_itinerary, save_budget, get_user_trips, get_user_bookings


def test_section_39_complete_travel_scenario():
    """
    Rigorously tests Section 39 requirements:
    Starting: Hyderabad, Destination: Araku Valley, Travelers: 2, Duration: 3 days,
    Budget: ₹20,000, Traveler Type: Couple, Interests: Nature + Photography,
    Transport: Train + Local Cab, Accommodation: Budget Hotel, Food: Local + Vegetarian.
    """
    origin = "Hyderabad"
    destination_name = "Araku Valley"
    travelers = 2
    days = 3
    user_budget = 20000.0
    traveler_type = "Couple"
    interests = ["Nature", "Photography"]
    user_id = 2

    # 1. Find destination & verify information
    dest = DestinationService.get_by_name_or_discover(destination_name)
    assert dest is not None
    assert dest["name"] == "Araku Valley"
    assert dest["state"] == "Andhra Pradesh"
    assert float(dest["latitude"]) > 0 and float(dest["longitude"]) > 0

    # 2. Destination weather & details
    weather = WeatherService.get_weather(float(dest["latitude"]), float(dest["longitude"]), dest["name"])
    assert "temperature" in weather
    assert "forecast" in weather

    details = DestinationService.get_details(dest["id"])
    assert len(details["attractions"]) >= 4
    assert len(details["hotels"]) >= 2
    assert len(details["activities"]) >= 2

    # 3. Find Transportation (Train)
    trains = TrainService.search_trains(origin, destination_name, "2026-09-20")
    assert len(trains) > 0
    selected_train = trains[0]
    transport_fare_person = selected_train["fare_3ac"]

    # 4. Find Accommodation (Budget Hotel)
    hotels = HotelService.search_hotels(dest["id"], hotel_type="Budget hotel")
    assert len(hotels) > 0
    selected_hotel = hotels[0]
    hotel_nightly = selected_hotel["price_per_night"]

    # 5. Find Activities & Entrance Fees
    attractions = details["attractions"]
    total_act_fee = sum(float(a.get("entry_fee", 0.0)) for a in attractions[:4])

    # 6. Generate 3-Day Itinerary
    itinerary = ItineraryService.generate_itinerary(
        destination_name=dest["name"],
        days=days,
        traveler_type=traveler_type,
        interests=interests,
        attractions=attractions,
        activities=details["activities"],
        hotel_name=selected_hotel["name"]
    )
    assert len(itinerary) >= 9 # Multiple events per day across 3 days
    scheduled_days = set(i["day"] for i in itinerary)
    assert scheduled_days == {1, 2, 3}

    # 7. Calculate Budget
    budget_calc = BudgetService.calculate_trip_budget(
        days=days,
        travelers=travelers,
        transport_fare_per_person=transport_fare_person,
        hotel_nightly_rate=hotel_nightly,
        food_style="Vegetarian",
        travel_style="Comfortable",
        activities_cost_per_person=total_act_fee,
        local_cab_daily_rate=1400.0
    )

    # 8. Check budget vs target ₹20,000
    assert budget_calc["total_estimated_cost"] > 0
    opt_result = BudgetService.optimize_budget(
        user_budget=user_budget,
        original_plan=budget_calc,
        days=days,
        travelers=travelers,
        current_transport_type="Train",
        current_hotel_price=hotel_nightly
    )

    active_plan = opt_result["optimized_plan"] if opt_result["needs_optimization"] else budget_calc
    # Total estimated cost must be within or very close to user budget
    assert active_plan["total_estimated_cost"] <= user_budget * 1.05

    # 9. Save the Trip
    trip_id = save_trip(
        user_id=user_id,
        trip_name="Araku Valley Couple Gateway",
        origin=origin,
        destination=destination_name,
        start_date="2026-09-20",
        end_date="2026-09-23",
        days=days,
        travelers_count=travelers,
        traveler_type=traveler_type,
        travel_style="Comfortable",
        allocated_budget=user_budget,
        total_estimated_cost=active_plan["total_estimated_cost"]
    )
    assert trip_id is not None
    save_itinerary(trip_id, itinerary)
    save_budget(
        trip_id=trip_id,
        transport_cost=active_plan["transport_cost"],
        accommodation_cost=active_plan["accommodation_cost"],
        food_cost=active_plan["food_cost"],
        activities_cost=active_plan["activities_cost"],
        local_transport_cost=active_plan["local_transport_cost"],
        buffer_cost=active_plan["buffer_cost"],
        total_cost=active_plan["total_estimated_cost"]
    )

    # 10. Perform In-App Bookings (Transport & Hotel)
    trans_booking = BookingService.book_ticket(
        user_id=user_id,
        category="Train",
        provider_name=selected_train["train_name"],
        item_title=f"Train #{selected_train['train_number']} (Hyderabad to Araku Valley)",
        travel_date="2026-09-20",
        passenger_count=travelers,
        total_amount=active_plan["transport_cost"],
        passengers=[{"name": "Traveler 1", "age": 28}, {"name": "Traveler 2", "age": 26}],
        trip_id=trip_id,
        payment_method="UPI Demo"
    )
    assert trans_booking["status"] == "Confirmed"
    assert trans_booking["booking_reference"].startswith("PNR-TRN")

    hotel_booking = BookingService.book_ticket(
        user_id=user_id,
        category="Hotel",
        provider_name=selected_hotel["name"],
        item_title=f"{selected_hotel['name']} (2 Nights)",
        travel_date="2026-09-20",
        passenger_count=travelers,
        total_amount=active_plan["accommodation_cost"],
        passengers=[{"name": "Traveler 1", "age": 28}],
        trip_id=trip_id,
        payment_method="UPI Demo"
    )
    assert hotel_booking["status"] == "Confirmed"
    assert hotel_booking["booking_reference"].startswith("BK-HTL")

    # 11. Verify in My Trips and My Bookings
    user_trips = get_user_trips(user_id)
    assert any(t["id"] == trip_id for t in user_trips)

    user_bookings = get_user_bookings(user_id)
    assert any(b["booking_reference"] == trans_booking["booking_reference"] for b in user_bookings)
    assert any(b["booking_reference"] == hotel_booking["booking_reference"] for b in user_bookings)
