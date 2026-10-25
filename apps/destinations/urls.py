from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/api/autocomplete/', views.destination_autocomplete, name='destination_autocomplete'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('destinations/<int:destination_id>/review/', views.add_review, name='add_review'),
]
