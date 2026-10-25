from django.urls import path
from . import views

urlpatterns = [
    path('plan-trip/', views.plan_trip, name='plan_trip'),
    path('trips/<int:trip_id>/itinerary/', views.trip_itinerary, name='trip_itinerary'),
    path('trips/<int:trip_id>/map/', views.trip_map, name='trip_map'),
    path('trips/proposal/<int:proposal_id>/action/', views.weather_adjustment_action, name='weather_adjustment_action'),
    path('my-trips/', views.my_trips, name='my_trips'),
]
