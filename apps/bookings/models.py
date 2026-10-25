import uuid
from django.db import models
from apps.accounts.models import User
from apps.destinations.models import Destination
from apps.trips.models import Trip

def generate_booking_reference():
    return f"BK-{uuid.uuid4().hex[:8].upper()}"

class Hotel(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels', limit_choices_to={'role': 'provider'})
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=200)
    address = models.TextField()
    star_rating = models.PositiveSmallIntegerField(default=4)
    cover_image = models.URLField(max_length=600)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=3500.00)
    cancellation_policy = models.CharField(max_length=255, default='Free cancellation up to 24 hours before check-in')
    amenities = models.TextField(default='Free WiFi, Swimming Pool, Air Conditioning, Complimentary Breakfast, Airport Shuttle')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=120) # Deluxe Room, Suite, Executive
    description = models.TextField(blank=True)
    capacity_guests = models.PositiveIntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField(default=10)
    available_rooms = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.name} @ {self.hotel.name} (₹{self.price_per_night}/night)"


class TransportService(models.Model):
    TYPE_CHOICES = (
        ('cab', 'Private Cab / Taxi'),
        ('bus', 'AC Sleeper / Semi-Sleeper Bus'),
        ('tourist_van', 'Tourist Tempo Traveler'),
        ('flight_train', 'Express Transit Shuttle'),
    )

    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_services', limit_choices_to={'role': 'provider'})
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='transports')
    service_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='cab')
    name = models.CharField(max_length=200) # e.g. Royal Travels AC Bus, Sedan Cab Service
    source_city = models.CharField(max_length=150)
    destination_city = models.CharField(max_length=150)
    departure_time = models.CharField(max_length=50, default='07:00 AM')
    estimated_arrival_time = models.CharField(max_length=50, default='02:00 PM')
    pickup_point = models.CharField(max_length=200, default='City Center Hub')
    drop_point = models.CharField(max_length=200, default='Main Hotel Zone')
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    total_capacity = models.PositiveIntegerField(default=20)
    available_capacity = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.source_city} -> {self.destination_city})"


class Activity(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', limit_choices_to={'role': 'provider'})
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='booked_activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=600)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=3.0)
    time_slot = models.CharField(max_length=100, default='10:00 AM - 01:00 PM')
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    total_capacity = models.PositiveIntegerField(default=25)
    available_slots = models.PositiveIntegerField(default=25)
    cancellation_policy = models.CharField(max_length=255, default='Cancel up to 12 hours before slot for full refund')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} in {self.destination.name}"


class Booking(models.Model):
    TYPE_CHOICES = (
        ('hotel', 'Hotel Room Reservation'),
        ('transport', 'Transport Service Reservation'),
        ('activity', 'Tourist Attraction / Activity Ticket'),
        ('package', 'Complete Trip Package'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected by Provider'),
        ('cancelled', 'Cancelled by Traveler'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(max_length=20, unique=True, default=generate_booking_reference)
    booking_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True)
    
    transport_service = models.ForeignKey(TransportService, on_delete=models.SET_NULL, null=True, blank=True)
    
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
    
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, help_text="Number of rooms, seats, or tickets")
    guests_count = models.PositiveIntegerField(default=1)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.get_booking_type_display()} ({self.user.username})"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('created', 'Order Created'),
        ('successful', 'Payment Captured / Verified'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    payment_mode = models.CharField(max_length=50, default='Razorpay Test Gateway / UPI / Card')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.razorpay_order_id} - {self.status}"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.action} by {self.user}"
