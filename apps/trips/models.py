from django.db import models
from apps.accounts.models import User
from apps.destinations.models import Destination, TouristAttraction

class Trip(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft / Saved'),
        ('confirmed', 'Confirmed & Booked'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    starting_location = models.CharField(max_length=150, default='Hyderabad')
    start_date = models.DateField()
    end_date = models.DateField()
    num_days = models.PositiveIntegerField(default=3)
    num_travelers = models.PositiveIntegerField(default=1)
    travel_style = models.CharField(max_length=50, default='Family')
    transport_preference = models.CharField(max_length=50, default='Cab / Taxi')
    accommodation_preference = models.CharField(max_length=50, default='3-Star / Boutique Hotel')
    dietary_notes = models.CharField(max_length=200, blank=True)
    accessibility_notes = models.CharField(max_length=200, blank=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=20000.00)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def remaining_budget(self):
        return self.total_budget - self.estimated_cost

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ItineraryDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    date = models.DateField()
    summary = models.TextField(blank=True)
    weather_condition = models.CharField(max_length=100, default='Clear Sky')
    forecast_temp = models.CharField(max_length=50, default='28°C')
    rain_probability = models.IntegerField(default=10, help_text="Percentage 0-100")

    class Meta:
        ordering = ['day_number']
        unique_together = ('trip', 'day_number')

    def __str__(self):
        return f"Day {self.day_number} - {self.trip.title}"


class ItineraryItem(models.Model):
    TIME_SLOT_CHOICES = (
        ('morning', 'Morning (08:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 05:00 PM)'),
        ('evening', 'Evening (05:00 PM - 09:00 PM)'),
    )

    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='items')
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.SET_NULL, null=True, blank=True)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='morning')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_outdoor = models.BooleanField(default=True)
    weather_status = models.CharField(max_length=30, default='normal', 
                                      choices=(('normal', 'Normal'), ('weather_alert', 'Weather Risk'), ('replaced', 'Alternative Suggested')))
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.get_time_slot_display()})"


class WeatherAdjustmentProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Traveler Review'),
        ('accepted', 'Accepted and Applied'),
        ('rejected', 'Rejected by Traveler'),
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='weather_adjustments')
    affected_day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE)
    weather_condition = models.CharField(max_length=100)
    reason = models.TextField()
    original_item_title = models.CharField(max_length=200)
    replacement_attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE)
    original_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    new_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cost_difference = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather adjustment for Trip {self.trip.id}: {self.original_item_title} -> {self.replacement_attraction.name}"
