from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Destination, TouristAttraction, DestinationReview
from apps.weather.services import get_destination_weather
from apps.bookings.models import Hotel, Activity, TransportService

def home(request):
    popular_destinations = Destination.objects.filter(is_popular=True)[:9]
    all_destinations = Destination.objects.all()
    featured_hotels = Hotel.objects.filter(is_active=True)[:6]
    featured_activities = Activity.objects.filter(is_active=True)[:6]
    
    # Weather teaser for 3 destinations
    weather_highlights = []
    for d in popular_destinations[:3]:
        w = get_destination_weather(d.name, float(d.latitude), float(d.longitude))
        weather_highlights.append({
            'destination': d,
            'weather': w['current'],
            'is_live': w['is_live'],
            'source_label': w['source_label']
        })

    context = {
        'popular_destinations': popular_destinations,
        'all_destinations': all_destinations,
        'featured_hotels': featured_hotels,
        'featured_activities': featured_activities,
        'weather_highlights': weather_highlights,
    }
    return render(request, 'home.html', context)


def destination_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    max_budget = request.GET.get('budget', '').strip()

    qs = Destination.objects.all()
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(state_country__icontains=query) | Q(description__icontains=query))
    if max_budget and max_budget.isdigit():
        qs = qs.filter(average_budget_per_day__lte=float(max_budget))

    destinations_with_weather = []
    for d in qs:
        w = get_destination_weather(d.name, float(d.latitude), float(d.longitude))
        destinations_with_weather.append({
            'dest': d,
            'weather': w['current'],
            'is_live': w['is_live']
        })

    return render(request, 'destinations/list.html', {
        'destinations': destinations_with_weather,
        'query': query,
        'budget': max_budget
    })


def destination_detail(request, slug):
    dest = Destination.objects.filter(slug=slug).first()
    if not dest:
        clean_name = slug.split('-')[0]
        dest = Destination.objects.filter(
            Q(slug__startswith=slug) | Q(name__icontains=clean_name)
        ).first()
    if not dest:
        dest = get_object_or_404(Destination, slug=slug)
    attractions = dest.attractions.all()
    hotels = dest.hotels.filter(is_active=True)[:3]
    activities = dest.booked_activities.filter(is_active=True)[:3]
    transports = dest.transports.filter(is_active=True)[:3]
    reviews = dest.reviews.order_by('-created_at')[:10]

    weather = get_destination_weather(dest.name, float(dest.latitude), float(dest.longitude))

    # Map markers data
    attraction_points = [
        {
            'name': a.name,
            'lat': float(a.latitude),
            'lng': float(a.longitude),
            'category': a.get_category_display(),
            'fee': f"₹{a.entry_fee}",
            'indoor': a.is_indoor,
            'desc': a.description[:120] + "..." if len(a.description) > 120 else a.description
        }
        for a in attractions
    ]

    context = {
        'dest': dest,
        'attractions': attractions,
        'hotels': hotels,
        'activities': activities,
        'transports': transports,
        'reviews': reviews,
        'weather': weather,
        'attraction_points': attraction_points,
    }
    return render(request, 'destinations/detail.html', context)


def destination_autocomplete(request):
    term = request.GET.get('term', '').strip()
    if not term:
        return JsonResponse([], safe=False)
    matches = Destination.objects.filter(
        Q(name__icontains=term) | Q(state_country__icontains=term) | Q(tagline__icontains=term)
    )[:10]
    data = [{'id': d.id, 'label': f"{d.name}, {d.state_country}", 'slug': d.slug} for d in matches]
    return JsonResponse(data, safe=False)


@login_required
def add_review(request, destination_id):
    dest = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            DestinationReview.objects.create(
                destination=dest,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Thank you for your destination review!")
    return redirect('destination_detail', slug=dest.slug)
