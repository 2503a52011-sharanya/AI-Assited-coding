from django.shortcuts import render
from django.http import JsonResponse
from apps.destinations.models import Destination
from .services import get_destination_weather

def weather_dashboard(request):
    selected_city = request.GET.get('city', 'Goa').strip()
    destinations = Destination.objects.all()

    target_dest = Destination.objects.filter(name__iexact=selected_city).first()
    lat = float(target_dest.latitude) if target_dest else None
    lon = float(target_dest.longitude) if target_dest else None

    force_refresh = request.GET.get('refresh') == '1'
    weather_data = get_destination_weather(selected_city, lat, lon, force_refresh=force_refresh)

    # Multi-destination overview cards
    cards = []
    for d in destinations[:6]:
        w = get_destination_weather(d.name, float(d.latitude), float(d.longitude))
        cards.append({
            'destination': d,
            'current': w['current'],
            'is_live': w['is_live']
        })

    context = {
        'selected_city': selected_city,
        'weather': weather_data,
        'destinations': destinations,
        'cards': cards,
    }
    return render(request, 'weather/dashboard.html', context)


def weather_api_view(request, city):
    force_refresh = request.GET.get('refresh') == '1'
    w = get_destination_weather(city, force_refresh=force_refresh)
    return JsonResponse(w)
