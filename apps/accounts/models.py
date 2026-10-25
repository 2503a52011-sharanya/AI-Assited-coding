from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('traveler', 'Traveler'),
        ('provider', 'Service Provider'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='traveler')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.URLField(max_length=500, blank=True, null=True, 
                                     default='https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80')

    @property
    def is_traveler(self):
        return self.role == 'traveler'

    @property
    def is_provider(self):
        return self.role == 'provider'

    @property
    def is_platform_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class TravelerProfile(models.Model):
    TRAVEL_STYLE_CHOICES = (
        ('Adventure', 'Adventure'),
        ('Nature', 'Nature'),
        ('Heritage', 'Heritage'),
        ('Religious', 'Religious'),
        ('Family', 'Family'),
        ('Romantic', 'Romantic'),
        ('Food', 'Food'),
        ('Shopping', 'Shopping'),
        ('Relaxation', 'Relaxation'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='traveler_profile')
    preferred_currency = models.CharField(max_length=10, default='INR')
    travel_style = models.CharField(max_length=50, choices=TRAVEL_STYLE_CHOICES, default='Family')
    dietary_preferences = models.CharField(max_length=100, blank=True, default='No special restriction')
    accessibility_needs = models.CharField(max_length=255, blank=True, default='None')
    emergency_contact = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, default='Passionate explorer eager to discover the world.')

    def __str__(self):
        return f"Profile of {self.user.username}"


class ProviderProfile(models.Model):
    BUSINESS_TYPE_CHOICES = (
        ('hotel', 'Hotels & Accommodation'),
        ('transport', 'Transport Services'),
        ('activity', 'Tours & Activities'),
        ('all', 'Complete Tourism Solutions'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPE_CHOICES, default='hotel')
    license_number = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    office_address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({'Approved' if self.is_approved else 'Pending Approval'})"
