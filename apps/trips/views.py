import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.destinations.models import Destination, TouristAttraction
from apps.weather.services import get_destination_weather
from apps.bookings.models import Hotel
from apps.notifications.models import send_notification
from .models import Trip, ItineraryDay, ItineraryItem, WeatherAdjustmentProposal

@login_required
def plan_trip(request):
    destinations = Destination.objects.all()

    if request.method == 'POST':
        dest_id = request.POST.get('destination')
        start_location = request.POST.get('starting_location', 'Hyderabad').strip()
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        num_travelers = int(request.POST.get('num_travelers', 1))
        budget = Decimal(request.POST.get('total_budget', 25000))
        travel_style = request.POST.get('travel_style', 'Family')
        transport_pref = request.POST.get('transport_preference', 'Cab / Taxi')
        accom_pref = request.POST.get('accommodation_preference', '3-Star / Boutique Hotel')
        dietary_notes = request.POST.get('dietary_notes', '').strip()
        accessibility_notes = request.POST.get('accessibility_notes', '').strip()

        # Validation
        if not dest_id or not start_date_str or not end_date_str:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'trips/planner.html', {'destinations': destinations})

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, 'trips/planner.html', {'destinations': destinations})

        if end_date < start_date:
            messages.error(request, "Return date cannot be earlier than departure date.")
            return render(request, 'trips/planner.html', {'destinations': destinations})

        destination = get_object_or_404(Destination, id=dest_id)
        num_days = (end_date - start_date).days + 1
        if num_days > 10:
            num_days = 10 # Cap to 10 days for realistic planning

        # Create Trip
        trip = Trip.objects.create(
            user=request.user,
            destination=destination,
            title=f"{num_days}-Day {travel_style} Trip to {destination.name}",
            starting_location=start_location,
            start_date=start_date,
            end_date=end_date,
            num_days=num_days,
            num_travelers=num_travelers,
            travel_style=travel_style,
            transport_preference=transport_pref,
            accommodation_preference=accom_pref,
            dietary_notes=dietary_notes,
            accessibility_notes=accessibility_notes,
            total_budget=budget,
            status='draft'
        )

        # Retrieve Weather forecast for the destination
        weather_info = get_destination_weather(destination.name, float(destination.latitude), float(destination.longitude))
        forecast_list = weather_info.get('forecast', [])

        # Retrieve available attractions
        all_attractions = list(destination.attractions.all())
        used_attraction_ids = set()

        total_estimated_cost = Decimal('0.00')

        # Thematic day descriptions for distinct daily plans
        day_themes = [
            f"Day 1: Arrival & Iconic Landmarks — Exploring panoramic lookouts and historic fortresses of {destination.name}.",
            f"Day 2: Cultural Immersion & Artistry — Discovering renowned museums, covered galleries, and royal palaces.",
            f"Day 3: Nature Escapes & Bazaars — Scenic waterfalls, spice trails, and vibrant local evening markets.",
            f"Day 4: Spiritual Sanctuaries & Living Heritage — Sacred architectural shrines and traditional craft centers.",
            f"Day 5: Leisure & Culinary Discoveries — Backwater/coastal promenades, local delicacies, and sunset experiences.",
            f"Day 6: Hidden Gems & Offbeat Trails — Scenic viewpoints and authentic countryside wanderings.",
            f"Day 7: Farewell & Artisan Souvenirs — Cultural farewell and relaxed scenic photography.",
        ]

        # Build Day-wise itineraries with completely distinct places
        for d in range(num_days):
            current_day_date = start_date + timedelta(days=d)
            
            # Match weather if available
            day_weather = "Pleasant & Clear"
            day_temp = "28°C"
            rain_prob = 10
            if d < len(forecast_list):
                day_weather = forecast_list[d].get('condition', 'Clear')
                day_temp = forecast_list[d].get('temp', '28°C')
                rain_prob = forecast_list[d].get('rain_chance', 15)

            theme_summary = day_themes[d % len(day_themes)]

            itinerary_day = ItineraryDay.objects.create(
                trip=trip,
                day_number=d + 1,
                date=current_day_date,
                summary=theme_summary,
                weather_condition=day_weather,
                forecast_temp=day_temp,
                rain_probability=rain_prob
            )

            # Slots: morning, afternoon, evening
            slots = [
                ('morning', '09:00 AM', '12:30 PM', ['Heritage', 'Nature', 'Adventure'], f"Morning Sightseeing & Historical Exploration"),
                ('afternoon', '02:00 PM', '05:00 PM', ['Museum', 'Heritage', 'Food'], f"Afternoon Cultural Gallery & Museum Visit"),
                ('evening', '05:30 PM', '08:30 PM', ['Shopping', 'Relaxation', 'Nature'], f"Evening Sunset Views, Bazaars & Promenade")
            ]

            for slot_key, st_time_str, end_time_str, preferred_categories, default_title in slots:
                # Pick an unused attraction prioritizing preferred category
                candidate = None
                
                # 1. Try unused matching category
                for a in all_attractions:
                    if a.id not in used_attraction_ids and a.category in preferred_categories:
                        candidate = a
                        break

                # 2. Try any unused attraction
                if not candidate:
                    for a in all_attractions:
                        if a.id not in used_attraction_ids:
                            candidate = a
                            break

                # 3. If all attractions in catalog are used, pick the least recently used
                if not candidate and all_attractions:
                    candidate = all_attractions[len(used_attraction_ids) % len(all_attractions)]

                if candidate:
                    used_attraction_ids.add(candidate.id)
                    attraction = candidate
                    item_title = candidate.name
                    item_desc = candidate.description
                    item_loc = candidate.name
                    item_lat = candidate.latitude
                    item_lng = candidate.longitude
                    is_outdoor_val = not candidate.is_indoor
                    cost = (candidate.entry_fee * num_travelers)
                else:
                    attraction = None
                    item_title = f"{default_title} in {destination.name}"
                    item_desc = f"Enjoy a curated leisure slot soaking in the local atmosphere of {destination.name}."
                    item_loc = f"{destination.name} Tourist Hub"
                    item_lat = destination.latitude
                    item_lng = destination.longitude
                    is_outdoor_val = True
                    cost = Decimal('150.00')

                total_estimated_cost += cost

                # Determine weather status
                w_status = 'normal'
                if rain_prob >= 70 and is_outdoor_val:
                    w_status = 'weather_alert'

                ItineraryItem.objects.create(
                    day=itinerary_day,
                    attraction=attraction,
                    time_slot=slot_key,
                    title=item_title,
                    description=item_desc,
                    location_name=item_loc,
                    latitude=item_lat,
                    longitude=item_lng,
                    estimated_cost=cost,
                    is_outdoor=is_outdoor_val,
                    weather_status=w_status,
                    order=1 if slot_key == 'morning' else (2 if slot_key == 'afternoon' else 3)
                )

        # Add estimated baseline for hotel & transport
        est_hotel_per_night = Decimal('3200.00')
        est_transport_daily = Decimal('1200.00')
        total_estimated_cost += (est_hotel_per_night * max(1, num_days - 1)) + (est_transport_daily * num_days)

        trip.estimated_cost = total_estimated_cost
        trip.save()

        # Check for automatic weather-based proposal if rain alerts were detected
        adverse_day = trip.days.filter(rain_probability__gte=60).first()
        if adverse_day:
            outdoor_item = adverse_day.items.filter(is_outdoor=True).first()
            if outdoor_item:
                indoor_alt = destination.attractions.filter(is_indoor=True).exclude(id=outdoor_item.attraction_id if outdoor_item.attraction else None).first()
                if not indoor_alt:
                    indoor_alt = destination.attractions.filter(rain_friendly=True).first()

                if indoor_alt:
                    orig_cost = outdoor_item.estimated_cost
                    new_c = indoor_alt.entry_fee * num_travelers
                    diff = new_c - orig_cost
                    WeatherAdjustmentProposal.objects.create(
                        trip=trip,
                        affected_day=adverse_day,
                        weather_condition=f"{adverse_day.weather_condition} ({adverse_day.rain_probability}% Rain Forecast)",
                        reason=f"High probability of precipitation ({adverse_day.rain_probability}%) detected on {adverse_day.date.strftime('%b %d')}. Outdoor activity '{outdoor_item.title}' may cause inconvenience or closure.",
                        original_item_title=outdoor_item.title,
                        replacement_attraction=indoor_alt,
                        original_cost=orig_cost,
                        new_cost=new_c,
                        cost_difference=diff,
                        status='pending'
                    )
                    send_notification(
                        request.user,
                        "Weather Advisory for Your Trip",
                        f"Forecast indicates rain during your trip to {destination.name}. An indoor alternative has been prepared for review.",
                        notification_type='weather',
                        link_url=f"/trips/{trip.id}/itinerary/"
                    )

        messages.success(request, f"AI personalized itinerary for {destination.name} generated successfully!")
        return redirect('trip_itinerary', trip_id=trip.id)

    return render(request, 'trips/planner.html', {'destinations': destinations})


@login_required
def trip_itinerary(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    days = trip.days.prefetch_related('items', 'items__attraction').all()
    weather_info = get_destination_weather(trip.destination.name, float(trip.destination.latitude), float(trip.destination.longitude))
    
    # Active weather proposals
    proposals = trip.weather_adjustments.filter(status='pending')
    hotels = trip.destination.hotels.filter(is_active=True)[:2]
    transports = trip.destination.transports.filter(is_active=True)[:2]

    context = {
        'trip': trip,
        'days': days,
        'weather_info': weather_info,
        'proposals': proposals,
        'hotels': hotels,
        'transports': transports,
    }
    return render(request, 'trips/itinerary.html', context)


@login_required
def weather_adjustment_action(request, proposal_id):
    proposal = get_object_or_404(WeatherAdjustmentProposal, id=proposal_id, trip__user=request.user)
    action = request.POST.get('action') # 'accept' or 'reject'

    if action == 'accept':
        proposal.status = 'accepted'
        proposal.save()

        # Update the itinerary item
        target_item = ItineraryItem.objects.filter(
            day=proposal.affected_day,
            title=proposal.original_item_title
        ).first()

        if target_item:
            alt = proposal.replacement_attraction
            target_item.attraction = alt
            target_item.title = alt.name
            target_item.description = f"[Weather Adjusted] {alt.description}"
            target_item.location_name = alt.name
            target_item.latitude = alt.latitude
            target_item.longitude = alt.longitude
            target_item.is_outdoor = not alt.is_indoor
            target_item.weather_status = 'replaced'
            target_item.estimated_cost = proposal.new_cost
            target_item.save()

            # Update trip budget
            trip = proposal.trip
            trip.estimated_cost += proposal.cost_difference
            trip.save()

        messages.success(request, f"Itinerary updated! Replaced '{proposal.original_item_title}' with indoor experience '{proposal.replacement_attraction.name}'.")
    else:
        proposal.status = 'rejected'
        proposal.save()
        messages.info(request, "Weather suggestion declined. Original itinerary retained.")

    return redirect('trip_itinerary', trip_id=proposal.trip.id)


@login_required
def trip_map(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    days = trip.days.prefetch_related('items', 'items__attraction').all()

    # Collect distinct places with sequence numbers
    points = []
    seq = 1

    # Add Starting Location marker
    points.append({
        'seq': 'Start',
        'name': f"Departure: {trip.starting_location}",
        'lat': float(trip.destination.latitude) - 0.05, # Representative pickup node
        'lng': float(trip.destination.longitude) - 0.05,
        'type': 'start',
        'details': f"Starting point for your journey"
    })

    # Recommended Hotel marker
    rec_hotel = trip.destination.hotels.first()
    if rec_hotel:
        points.append({
            'seq': 'Hotel',
            'name': rec_hotel.name,
            'lat': float(trip.destination.latitude) + 0.015,
            'lng': float(trip.destination.longitude) + 0.012,
            'type': 'hotel',
            'details': f"{rec_hotel.star_rating}-Star Stay: {rec_hotel.address}"
        })

    # Add each itinerary stop
    for day in days:
        for item in day.items.all():
            points.append({
                'seq': seq,
                'name': item.title,
                'lat': float(item.latitude),
                'lng': float(item.longitude),
                'type': 'attraction',
                'day': day.day_number,
                'time_slot': item.get_time_slot_display(),
                'cost': f"₹{item.estimated_cost}",
                'details': item.description[:150] + "..." if len(item.description) > 150 else item.description,
                'is_outdoor': item.is_outdoor,
                'weather_status': item.weather_status
            })
            seq += 1

    context = {
        'trip': trip,
        'points_json': json.dumps(points),
        'points': points,
        'days': days,
    }
    return render(request, 'trips/map.html', context)


@login_required
def my_trips(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'trips/my_trips.html', {'trips': trips})
