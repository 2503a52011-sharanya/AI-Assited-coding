from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_dashboard, name='weather_dashboard'),
    path('api/weather/<str:city>/', views.weather_api_view, name='weather_api'),
]
