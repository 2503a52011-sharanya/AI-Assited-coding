import pytest
from services.booking_service import BookingService
from config.database import init_db


def test_booking_workflow():
    init_db()
    res = BookingService.book_ticket(
        user_id=2,
        category="Train",
        provider_name="Visakha Express",
        item_title="Hyderabad to Araku Valley (3AC)",
        travel_date="2026-09-20",
        passenger_count=2,
        total_amount=2400.0,
        passengers=[{"name": "Rohit Sharma", "age": 28, "seat": "B1-21"}, {"name": "Pooja Sharma", "age": 26, "seat": "B1-22"}],
        payment_method="Demo UPI"
    )

    assert res["status"] == "Confirmed"
    assert "booking_reference" in res
    assert res["booking_reference"].startswith("PNR-TRN")

    # Verify retrieval
    user_bookings = BookingService.get_user_bookings(user_id=2, category="Train")
    assert any(b["booking_reference"] == res["booking_reference"] for b in user_bookings)
