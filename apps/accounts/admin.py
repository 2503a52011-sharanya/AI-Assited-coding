from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TravelerProfile, ProviderProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone', 'profile_image')}),
    )

@admin.register(TravelerProfile)
class TravelerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_style', 'preferred_currency')

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'business_type', 'is_approved')
    list_filter = ('business_type', 'is_approved')
