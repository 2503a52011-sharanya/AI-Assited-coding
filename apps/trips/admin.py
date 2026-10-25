from django.contrib import admin
from .models import Trip, ItineraryDay, ItineraryItem, WeatherAdjustmentProposal

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'total_budget', 'status')
    list_filter = ('status', 'travel_style', 'destination')

@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ('trip', 'day_number', 'date', 'weather_condition')
    inlines = [ItineraryItemInline]

@admin.register(WeatherAdjustmentProposal)
class WeatherAdjustmentProposalAdmin(admin.ModelAdmin):
    list_display = ('trip', 'affected_day', 'original_item_title', 'status', 'cost_difference')
    list_filter = ('status',)
