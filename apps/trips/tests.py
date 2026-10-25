from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from decimal import Decimal
from apps.accounts.models import User
from apps.destinations.models import Destination, TouristAttraction
from apps.trips.models import Trip, ItineraryDay, ItineraryItem, WeatherAdjustmentProposal
from apps.bookings.models import Hotel, RoomType, TransportService, Activity, Booking, Payment
from apps.ai_assistant.services import generate_ai_travel_response
from apps.ai_assistant.models import ChatSession

class SmartTourismWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Traveler User
        self.traveler = User.objects.create_user(
            username='test_traveler',
            password='password123',
            email='traveler@test.com',
            role='traveler'
        )

        # 2. Provider User
        self.provider = User.objects.create_user(
            username='test_provider',
            password='password123',
            email='provider@test.com',
            role='provider'
        )

        # 3. Admin User
        self.admin = User.objects.create_superuser(
            username='test_admin',
            password='password123',
            email='admin@test.com',
            role='admin'
        )

        # Destination
        self.destination = Destination.objects.create(
            name='Goa Test',
            state_country='India',
            tagline='Coastal Paradise',
            description='Tropical beaches and historic chapels.',
            cover_image='https://example.com/goa.jpg',
            latitude=Decimal('15.498900'),
            longitude=Decimal('73.827800'),
            best_time_to_visit='Nov-Feb',
            average_budget_per_day=Decimal('4000.00'),
            is_popular=True
        )

        # Outdoor Attraction
        self.outdoor_attraction = TouristAttraction.objects.create(
            destination=self.destination,
            name='Sunny Beach Front',
            category='Nature',
            description='Outdoor beach walking with ocean waves.',
            image_url='https://example.com/beach.jpg',
            latitude=Decimal('15.540000'),
            longitude=Decimal('73.750000'),
            entry_fee=Decimal('0.00'),
            is_indoor=False,
            rain_friendly=False
        )

        # Indoor Attraction (for weather adjustment)
        self.indoor_attraction = TouristAttraction.objects.create(
            destination=self.destination,
            name='Indoor Heritage Museum',
            category='Museum',
            description='Historic museum with sheltered halls.',
            image_url='https://example.com/museum.jpg',
            latitude=Decimal('15.500000'),
            longitude=Decimal('73.910000'),
            entry_fee=Decimal('100.00'),
            is_indoor=True,
            rain_friendly=True
        )

        # Hotel & Room
        self.hotel = Hotel.objects.create(
            provider=self.provider,
            destination=self.destination,
            name='Grand Test Resort',
            address='123 Beach Road',
            star_rating=5,
            cover_image='https://example.com/resort.jpg',
            base_price=Decimal('4000.00')
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Deluxe Room',
            price_per_night=Decimal('4000.00'),
            total_rooms=5,
            available_rooms=5
        )

    def test_traveler_login(self):
        logged_in = self.client.login(username='test_traveler', password='password123')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)

    def test_admin_dashboard_security(self):
        # Ordinary traveler should be denied access (403 Forbidden)
        self.client.login(username='test_traveler', password='password123')
        res = self.client.get(reverse('portal_admin_dashboard'))
        self.assertEqual(res.status_code, 403)

        # Admin user must be granted access (200 OK)
        self.client.login(username='test_admin', password='password123')
        res_admin = self.client.get(reverse('portal_admin_dashboard'))
        self.assertEqual(res_admin.status_code, 200)

    def test_plan_trip_and_itinerary_creation(self):
        self.client.login(username='test_traveler', password='password123')
        today = datetime.now().date() + timedelta(days=1)
        end_date = today + timedelta(days=2)

        res = self.client.post(reverse('plan_trip'), {
            'destination': self.destination.id,
            'starting_location': 'Hyderabad',
            'start_date': today.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'num_travelers': 2,
            'total_budget': 30000,
            'travel_style': 'Family'
        })
        self.assertEqual(res.status_code, 302) # Redirect to itinerary view

        trip = Trip.objects.filter(user=self.traveler).first()
        self.assertIsNotNone(trip)
        self.assertEqual(trip.num_days, 3)
        self.assertEqual(trip.days.count(), 3)
        self.assertTrue(trip.days.first().items.count() > 0)

    def test_weather_adjustment_proposal_accept(self):
        # Create a trip with rain probability on day 1
        today = datetime.now().date() + timedelta(days=1)
        trip = Trip.objects.create(
            user=self.traveler,
            destination=self.destination,
            title='Rainy Test Trip',
            start_date=today,
            end_date=today + timedelta(days=1),
            num_days=2,
            num_travelers=1,
            total_budget=Decimal('20000.00'),
            estimated_cost=Decimal('5000.00')
        )
        day1 = ItineraryDay.objects.create(
            trip=trip,
            day_number=1,
            date=today,
            weather_condition='Heavy Rain',
            forecast_temp='27°C',
            rain_probability=85
        )
        item1 = ItineraryItem.objects.create(
            day=day1,
            attraction=self.outdoor_attraction,
            time_slot='morning',
            title=self.outdoor_attraction.name,
            location_name='Beach Zone',
            latitude=self.outdoor_attraction.latitude,
            longitude=self.outdoor_attraction.longitude,
            estimated_cost=Decimal('0.00'),
            is_outdoor=True,
            weather_status='weather_alert'
        )

        proposal = WeatherAdjustmentProposal.objects.create(
            trip=trip,
            affected_day=day1,
            weather_condition='Heavy Monsoon Rain (85% Rain Forecast)',
            reason='Rain prevents outdoor beach visit.',
            original_item_title=item1.title,
            replacement_attraction=self.indoor_attraction,
            original_cost=Decimal('0.00'),
            new_cost=Decimal('100.00'),
            cost_difference=Decimal('100.00'),
            status='pending'
        )

        # Login and accept proposal
        self.client.login(username='test_traveler', password='password123')
        res = self.client.post(reverse('weather_adjustment_action', kwargs={'proposal_id': proposal.id}), {
            'action': 'accept'
        })
        self.assertEqual(res.status_code, 302)

        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

        item1.refresh_from_db()
        self.assertEqual(item1.title, self.indoor_attraction.name)
        self.assertEqual(item1.weather_status, 'replaced')
        self.assertFalse(item1.is_outdoor)

    def test_booking_and_atomic_inventory_locking(self):
        self.client.login(username='test_traveler', password='password123')
        today = datetime.now().date() + timedelta(days=2)
        end_date = today + timedelta(days=3)

        # Initial available rooms
        self.assertEqual(self.room_type.available_rooms, 5)

        # Step 1: Book Hotel Room
        res = self.client.post(reverse('hotel_book', kwargs={'hotel_id': self.hotel.id}), {
            'room_type': self.room_type.id,
            'check_in': today.strftime('%Y-%m-%d'),
            'check_out': end_date.strftime('%Y-%m-%d'),
            'rooms_count': 2,
            'guests_count': 2
        })
        self.assertEqual(res.status_code, 302)

        booking = Booking.objects.filter(user=self.traveler, booking_type='hotel').first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.status, 'pending')
        self.assertFalse(booking.is_paid)

        # Step 2: Payment verification and atomic inventory reduction
        res_pay = self.client.post(reverse('payment_verify', kwargs={'booking_id': booking.id}), {
            'razorpay_order_id': f"order_{booking.booking_reference}",
            'razorpay_payment_id': 'pay_test_unit_12345',
            'razorpay_signature': 'valid_hmac_sig'
        })
        self.assertEqual(res_pay.status_code, 302)

        booking.refresh_from_db()
        self.assertTrue(booking.is_paid)
        self.assertEqual(booking.status, 'confirmed')

        # Verify Room Inventory was safely decremented by 2
        self.room_type.refresh_from_db()
        self.assertEqual(self.room_type.available_rooms, 3)

        # Step 3: Cancellation releases inventory
        res_cancel = self.client.post(reverse('booking_cancel', kwargs={'booking_id': booking.id}), {
            'cancellation_reason': 'Change of plans'
        })
        self.assertEqual(res_cancel.status_code, 302)

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

        # Verify Room Inventory was safely restored back to 5
        self.room_type.refresh_from_db()
        self.assertEqual(self.room_type.available_rooms, 5)

    def test_ai_chatbot_knowledge_response(self):
        session = ChatSession.objects.create(session_id='test_session_uuid', user=self.traveler)
        reply = generate_ai_travel_response(self.traveler, session, "What is the weather like in Goa?")
        self.assertIn("Goa", reply)
        self.assertTrue("Weather" in reply or "°C" in reply or "Clear" in reply)
