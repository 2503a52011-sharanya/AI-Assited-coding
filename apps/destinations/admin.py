from django.contrib import admin
from .models import Destination, TouristAttraction, DestinationReview

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'state_country', 'average_budget_per_day', 'is_popular')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'state_country')

@admin.register(TouristAttraction)
class TouristAttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'category', 'entry_fee', 'is_indoor', 'rain_friendly')
    list_filter = ('category', 'is_indoor', 'rain_friendly', 'destination')
    search_fields = ('name', 'destination__name')

@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'created_at')
