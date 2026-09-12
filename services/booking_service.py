import logging
from database.queries import create_booking, record_payment, execute_query, get_user_bookings, cancel_booking
from services.payment_service import PaymentService
from utils.helpers import generate_reference_id

logger = logging.getLogger(__name__)


class BookingService:
    @staticmethod
    def book_ticket(
        user_id: int,
        category: str, # Flight, Train, Bus, Hotel, Cab, Activity
        provider_name: str,
        item_title: str,
        travel_date: str,
        passenger_count: int,
        total_amount: float,
        passengers: list,
        trip_id: int = None,
        payment_method: str = "UPI (Demo Gateway)"
    ) -> dict:
        """Executes complete in-app booking workflow including payment and ticket generation."""
        # 1. Generate PNR / Reference ID
        prefix_map = {
            "Flight": "BK-FLT",
            "Train": "PNR-TRN",
            "Bus": "BK-BUS",
            "Hotel": "BK-HTL",
            "Cab": "BK-CAB",
            "Activity": "BK-ACT"
        }
        ref_prefix = prefix_map.get(category, "BK-TRV")
        booking_ref = generate_reference_id(ref_prefix)

        # 2. Process Payment via PaymentService
        tx = PaymentService.initiate_transaction(total_amount, booking_ref, method=payment_method)
        pay_res = PaymentService.process_payment(tx["payment_reference"], total_amount, method=payment_method)

        # 3. Save Booking to Database
        booking_id = create_booking(
            user_id=user_id,
            trip_id=trip_id,
            booking_ref=booking_ref,
            category=category,
            provider=provider_name,
            item_title=item_title,
            travel_date=travel_date,
            passenger_count=passenger_count,
            total_amount=total_amount,
            is_demo=True
        )

        # 4. Save Passengers / Guests
        for p in passengers:
            execute_query("""
            INSERT INTO booking_items (booking_id, passenger_name, passenger_age, seat_or_room)
            VALUES (:bid, :pname, :page, :seat)
            """, {
                "bid": booking_id,
                "pname": p.get("name", "Traveler"),
                "page": p.get("age", 28),
                "seat": p.get("seat", "Confirmed")
            })

        # 5. Record Payment
        record_payment(
            booking_id=booking_id,
            payment_ref=pay_res["payment_reference"],
            amount=total_amount,
            method=payment_method,
            status=pay_res["status"]
        )

        return {
            "booking_id": booking_id,
            "booking_reference": booking_ref,
            "category": category,
            "provider_name": provider_name,
            "item_title": item_title,
            "travel_date": travel_date,
            "passenger_count": passenger_count,
            "total_amount": total_amount,
            "payment_reference": pay_res["payment_reference"],
            "status": "Confirmed",
            "is_demo": True
        }

    @staticmethod
    def get_user_bookings(user_id: int, category: str = None):
        return get_user_bookings(user_id, category=category)

    @staticmethod
    def cancel_ticket(booking_id: int, user_id: int):
        cancel_booking(booking_id, user_id)
        return True
