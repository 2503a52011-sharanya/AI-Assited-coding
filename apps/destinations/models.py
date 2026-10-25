from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User

class Destination(models.Model):
    name = models.CharField(max_length=150, unique=True)
    state_country = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    cover_image = models.URLField(max_length=600)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    best_time_to_visit = models.CharField(max_length=150, default='October to March')
    average_budget_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.state_country}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state_country}"


class TouristAttraction(models.Model):
    CATEGORY_CHOICES = (
        ('Heritage', 'Heritage & Architecture'),
        ('Nature', 'Nature & Beaches'),
        ('Adventure', 'Adventure & Outdoor'),
        ('Religious', 'Religious & Spiritual'),
        ('Museum', 'Museum & Art Gallery'),
        ('Shopping', 'Local Markets & Shopping'),
        ('Food', 'Culinary & Dining'),
        ('Relaxation', 'Parks & Scenic Viewpoints'),
    )

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='Heritage')
    description = models.TextField()
    image_url = models.URLField(max_length=600)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    typical_time_spent_hours = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_indoor = models.BooleanField(default=False, help_text="True if sheltered/indoor")
    rain_friendly = models.BooleanField(default=False, help_text="Good alternative during rainy/adverse weather")
    accessibility_support = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"


class DestinationReview(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.destination.name}"
