from django.urls import path
from . import views

urlpatterns = [
    # Hotels
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/<int:hotel_id>/book/', views.hotel_book, name='hotel_book'),

    # Transport
    path('transport/', views.transport_list, name='transport_list'),
    path('transport/<int:transport_id>/book/', views.transport_book, name='transport_book'),

    # Activities
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/<int:activity_id>/book/', views.activity_book, name='activity_book'),

    # Trip package
    path('trips/<int:trip_id>/book-package/', views.trip_package_book, name='trip_package_book'),

    # Checkout & Payment
    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('checkout/<int:booking_id>/verify/', views.payment_verify, name='payment_verify'),

    # Bookings Dashboard & Voucher
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('bookings/<int:booking_id>/voucher/', views.booking_voucher, name='booking_voucher'),

    # Provider Portal
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/bookings/<int:booking_id>/action/', views.provider_booking_action, name='provider_booking_action'),

    # Administrator Dashboard
    path('portal-admin/dashboard/', views.portal_admin_dashboard, name='portal_admin_dashboard'),
    path('portal-admin/provider/<int:provider_id>/action/', views.admin_approve_provider, name='admin_approve_provider'),
]
