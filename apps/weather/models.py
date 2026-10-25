from django.db import models

class WeatherCache(models.Model):
    city = models.CharField(max_length=150, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    current_data = models.JSONField(default=dict)
    forecast_data = models.JSONField(default=list)
    is_live_api = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather for {self.city} ({'Live API' if self.is_live_api else 'Demo Mode'})"
