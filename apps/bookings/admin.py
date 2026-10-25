from django.contrib import admin
from .models import Hotel, RoomType, TransportService, Activity, Booking, Payment, AuditLog

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'provider', 'star_rating', 'is_active')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'price_per_night', 'available_rooms', 'total_rooms')

@admin.register(TransportService)
class TransportServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'source_city', 'destination_city', 'price_per_seat', 'available_capacity')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'provider', 'price_per_person', 'available_slots')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'booking_type', 'status', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('booking_type', 'status', 'is_paid')
    search_fields = ('booking_reference', 'user__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_order_id', 'booking', 'amount', 'status', 'created_at')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'user')
