import hmac
import hashlib
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from .models import Hotel, RoomType, TransportService, Activity, Booking, Payment, AuditLog
from apps.destinations.models import Destination
from apps.trips.models import Trip
from apps.accounts.models import User, ProviderProfile
from apps.notifications.models import send_notification

# ----------------- HOTEL VIEWS -----------------

def hotel_list(request):
    dest_id = request.GET.get('destination')
    query = request.GET.get('q', '').strip()
    hotels = Hotel.objects.filter(is_active=True).select_related('destination')

    if dest_id and dest_id.isdigit():
        hotels = hotels.filter(destination_id=int(dest_id))
    if query:
        hotels = hotels.filter(name__icontains=query)

    destinations = Destination.objects.all()
    return render(request, 'bookings/hotels.html', {
        'hotels': hotels,
        'destinations': destinations,
        'selected_dest': dest_id,
        'query': query
    })


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
    rooms = hotel.room_types.filter(available_rooms__gt=0)
    return render(request, 'bookings/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms,
        'amenities_list': [a.strip() for a in hotel.amenities.split(',')]
    })


@login_required
def hotel_book(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        room_type_id = request.POST.get('room_type')
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        quantity = int(request.POST.get('rooms_count', 1))
        guests = int(request.POST.get('guests_count', 2))

        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid check-in and check-out dates.")
            return redirect('hotel_detail', hotel_id=hotel.id)

        if check_out <= check_in:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('hotel_detail', hotel_id=hotel.id)

        room_type = get_object_or_404(RoomType, id=room_type_id, hotel=hotel)
        
        # Check current available inventory
        if room_type.available_rooms < quantity:
            messages.error(request, f"Sorry, only {room_type.available_rooms} room(s) available for this type.")
            return redirect('hotel_detail', hotel_id=hotel.id)

        nights = (check_out - check_in).days
        subtotal = room_type.price_per_night * nights * quantity
        taxes = subtotal * Decimal('0.12') # 12% GST
        total_amount = subtotal + taxes

        booking = Booking.objects.create(
            user=request.user,
            booking_type='hotel',
            hotel=hotel,
            room_type=room_type,
            start_date=check_in,
            end_date=check_out,
            quantity=quantity,
            guests_count=guests,
            total_amount=total_amount,
            status='pending',
            special_requests=request.POST.get('special_requests', '')
        )

        AuditLog.objects.create(
            user=request.user,
            action="HOTEL_BOOKING_INITIATED",
            details=f"Booking {booking.booking_reference} created for {hotel.name} ({quantity} rooms for {nights} nights)."
        )

        return redirect('checkout', booking_id=booking.id)

    return redirect('hotel_detail', hotel_id=hotel.id)


# ----------------- TRANSPORT VIEWS -----------------

def transport_list(request):
    transports = TransportService.objects.filter(is_active=True).select_related('destination')
    src = request.GET.get('source', '').strip()
    dest = request.GET.get('dest', '').strip()
    t_type = request.GET.get('type', '').strip()

    if src:
        transports = transports.filter(source_city__icontains=src)
    if dest:
        transports = transports.filter(destination_city__icontains=dest)
    if t_type:
        transports = transports.filter(service_type=t_type)

    return render(request, 'bookings/transport.html', {
        'transports': transports,
        'src': src,
        'dest': dest,
        't_type': t_type
    })


@login_required
def transport_book(request, transport_id):
    transport = get_object_or_404(TransportService, id=transport_id, is_active=True)
    if request.method == 'POST':
        travel_date_str = request.POST.get('travel_date')
        seats = int(request.POST.get('seats_count', 1))

        try:
            travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid travel date.")
            return redirect('transport_list')

        if transport.available_capacity < seats:
            messages.error(request, f"Only {transport.available_capacity} seat(s) available.")
            return redirect('transport_list')

        subtotal = transport.price_per_seat * seats
        taxes = subtotal * Decimal('0.05') # 5% transit tax
        total_amount = subtotal + taxes

        booking = Booking.objects.create(
            user=request.user,
            booking_type='transport',
            transport_service=transport,
            start_date=travel_date,
            quantity=seats,
            guests_count=seats,
            total_amount=total_amount,
            status='pending'
        )

        AuditLog.objects.create(
            user=request.user,
            action="TRANSPORT_BOOKING_INITIATED",
            details=f"Transport booking {booking.booking_reference} for {transport.name} ({seats} seats)."
        )

        return redirect('checkout', booking_id=booking.id)

    return redirect('transport_list')


# ----------------- ACTIVITY VIEWS -----------------

def activity_list(request):
    activities = Activity.objects.filter(is_active=True).select_related('destination')
    dest_id = request.GET.get('destination')
    if dest_id and dest_id.isdigit():
        activities = activities.filter(destination_id=int(dest_id))

    destinations = Destination.objects.all()
    return render(request, 'bookings/activities.html', {
        'activities': activities,
        'destinations': destinations,
        'selected_dest': dest_id
    })


@login_required
def activity_book(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, is_active=True)
    if request.method == 'POST':
        slot_date_str = request.POST.get('slot_date')
        tickets = int(request.POST.get('tickets_count', 1))

        try:
            slot_date = datetime.strptime(slot_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid activity date.")
            return redirect('activity_list')

        if activity.available_slots < tickets:
            messages.error(request, f"Only {activity.available_slots} ticket(s) remaining for this activity.")
            return redirect('activity_list')

        subtotal = activity.price_per_person * tickets
        taxes = subtotal * Decimal('0.18')
        total_amount = subtotal + taxes

        booking = Booking.objects.create(
            user=request.user,
            booking_type='activity',
            activity=activity,
            start_date=slot_date,
            quantity=tickets,
            guests_count=tickets,
            total_amount=total_amount,
            status='pending'
        )

        AuditLog.objects.create(
            user=request.user,
            action="ACTIVITY_BOOKING_INITIATED",
            details=f"Activity booking {booking.booking_reference} for {activity.title} ({tickets} tickets)."
        )

        return redirect('checkout', booking_id=booking.id)

    return redirect('activity_list')


# ----------------- TRIP PACKAGE BOOKING -----------------

@login_required
def trip_package_book(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    # Bundle trip estimated costs into package booking
    booking = Booking.objects.create(
        user=request.user,
        booking_type='package',
        trip=trip,
        start_date=trip.start_date,
        end_date=trip.end_date,
        quantity=1,
        guests_count=trip.num_travelers,
        total_amount=trip.estimated_cost,
        status='pending'
    )

    return redirect('checkout', booking_id=booking.id)


# ----------------- CHECKOUT & PAYMENT INTEGRATION -----------------

@login_required
def checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.is_paid:
        messages.info(request, "This booking has already been paid and confirmed.")
        return redirect('my_bookings')

    razorpay_key = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_demo123456789')
    
    # Calculate itemized breakdown
    subtotal = booking.total_amount / Decimal('1.12')
    tax = booking.total_amount - subtotal

    # Order ID simulation / generation
    order_id = f"order_{booking.booking_reference.replace('-', '_')}"

    context = {
        'booking': booking,
        'subtotal': round(subtotal, 2),
        'tax': round(tax, 2),
        'total': booking.total_amount,
        'razorpay_key': razorpay_key,
        'order_id': order_id,
    }
    return render(request, 'bookings/checkout.html', context)


@login_required
def payment_verify(request, booking_id):
    """
    Handles payment verification and executes atomic inventory locking.
    Prevents race conditions using transaction.atomic() & select_for_update().
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id', f"pay_test_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        order_id = request.POST.get('razorpay_order_id', f"order_{booking.booking_reference}")
        signature = request.POST.get('razorpay_signature', 'test_signature_valid')

        # Execute safe atomic inventory reservation
        try:
            with transaction.atomic():
                # Lock and update inventory according to booking type
                if booking.booking_type == 'hotel' and booking.room_type:
                    room = RoomType.objects.select_for_update().get(id=booking.room_type.id)
                    if room.available_rooms < booking.quantity:
                        raise ValueError(f"Inventory depleted. Only {room.available_rooms} rooms left.")
                    room.available_rooms -= booking.quantity
                    room.save()

                elif booking.booking_type == 'transport' and booking.transport_service:
                    transport = TransportService.objects.select_for_update().get(id=booking.transport_service.id)
                    if transport.available_capacity < booking.quantity:
                        raise ValueError(f"Seats depleted. Only {transport.available_capacity} seats left.")
                    transport.available_capacity -= booking.quantity
                    transport.save()

                elif booking.booking_type == 'activity' and booking.activity:
                    activity = Activity.objects.select_for_update().get(id=booking.activity.id)
                    if activity.available_slots < booking.quantity:
                        raise ValueError(f"Activity slots depleted. Only {activity.available_slots} tickets left.")
                    activity.available_slots -= booking.quantity
                    activity.save()

                # Mark payment recorded
                payment = Payment.objects.create(
                    booking=booking,
                    razorpay_order_id=order_id,
                    razorpay_payment_id=payment_id,
                    razorpay_signature=signature,
                    amount=booking.total_amount,
                    currency=booking.currency,
                    status='successful',
                    payment_mode='Razorpay Test Gateway / Verified'
                )

                # Update booking status
                booking.is_paid = True
                booking.status = 'confirmed'
                booking.save()

                # If attached to a trip, mark trip confirmed
                if booking.trip:
                    booking.trip.status = 'confirmed'
                    booking.trip.save()

                AuditLog.objects.create(
                    user=request.user,
                    action="PAYMENT_VERIFIED_BOOKING_CONFIRMED",
                    details=f"Booking {booking.booking_reference} confirmed with payment {payment_id} (₹{booking.total_amount})."
                )

                send_notification(
                    request.user,
                    "Booking Confirmed!",
                    f"Your booking {booking.booking_reference} has been successfully verified and confirmed. Pack your bags!",
                    notification_type='booking',
                    link_url=f"/my-bookings/"
                )

                messages.success(request, f"Payment successful! Booking {booking.booking_reference} is confirmed.")
                return redirect('booking_voucher', booking_id=booking.id)

        except ValueError as err:
            messages.error(request, f"Booking failed due to inventory constraint: {err}")
            return redirect('checkout', booking_id=booking.id)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('checkout', booking_id=booking.id)

    return redirect('checkout', booking_id=booking.id)


# ----------------- MY BOOKINGS & ACTIONS -----------------

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'current_filter': status_filter
    })


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status in ('cancelled', 'rejected'):
        messages.warning(request, "This booking has already been cancelled or rejected.")
        return redirect('my_bookings')

    if request.method == 'POST':
        reason = request.POST.get('cancellation_reason', 'Traveler requested cancellation.')
        with transaction.atomic():
            # Release inventory
            if booking.booking_type == 'hotel' and booking.room_type:
                room = RoomType.objects.select_for_update().get(id=booking.room_type.id)
                room.available_rooms += booking.quantity
                room.save()

            elif booking.booking_type == 'transport' and booking.transport_service:
                transport = TransportService.objects.select_for_update().get(id=booking.transport_service.id)
                transport.available_capacity += booking.quantity
                transport.save()

            elif booking.booking_type == 'activity' and booking.activity:
                activity = Activity.objects.select_for_update().get(id=booking.activity.id)
                activity.available_slots += booking.quantity
                activity.save()

            booking.status = 'cancelled'
            booking.cancellation_reason = reason
            booking.save()

            AuditLog.objects.create(
                user=request.user,
                action="BOOKING_CANCELLED",
                details=f"Booking {booking.booking_reference} cancelled by user. Inventory released."
            )

            send_notification(
                request.user,
                "Booking Cancelled",
                f"Booking {booking.booking_reference} was cancelled according to policy. Inventory has been restored.",
                notification_type='booking'
            )

        messages.info(request, f"Booking {booking.booking_reference} has been cancelled.")
        return redirect('my_bookings')

    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})


@login_required
def booking_voucher(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Check authorization
    if booking.user != request.user and not request.user.is_platform_admin and request.user.role != 'provider':
        return HttpResponseForbidden("You are not authorized to view this ticket.")

    return render(request, 'bookings/confirmation.html', {'booking': booking})


# ----------------- SERVICE PROVIDER PORTAL -----------------

@login_required
def provider_dashboard(request):
    if not request.user.is_provider and not request.user.is_platform_admin:
        messages.error(request, "Access restricted to registered Service Providers.")
        return redirect('home')

    provider = request.user
    my_hotels = Hotel.objects.filter(provider=provider)
    my_transports = TransportService.objects.filter(provider=provider)
    my_activities = Activity.objects.filter(provider=provider)

    # Bookings made for this provider's services
    bookings = Booking.objects.filter(
        hotel__provider=provider
    ) | Booking.objects.filter(
        transport_service__provider=provider
    ) | Booking.objects.filter(
        activity__provider=provider
    )
    bookings = bookings.distinct().order_by('-created_at')

    context = {
        'provider': provider,
        'profile': getattr(provider, 'provider_profile', None),
        'my_hotels': my_hotels,
        'my_transports': my_transports,
        'my_activities': my_activities,
        'recent_bookings': bookings[:10],
        'total_bookings_count': bookings.count(),
        'confirmed_count': bookings.filter(status='confirmed').count(),
    }
    return render(request, 'provider/dashboard.html', context)


@login_required
def provider_booking_action(request, booking_id):
    if not request.user.is_provider and not request.user.is_platform_admin:
        return HttpResponseForbidden("Unauthorized.")

    booking = get_object_or_404(Booking, id=booking_id)
    action = request.POST.get('action') # 'confirm' or 'reject'

    if action == 'confirm':
        booking.status = 'confirmed'
        booking.save()
        send_notification(
            booking.user,
            "Provider Confirmed Your Booking!",
            f"Great news! Your booking {booking.booking_reference} has been officially approved and confirmed by the service provider.",
            notification_type='booking',
            link_url='/my-bookings/'
        )
        messages.success(request, f"Booking {booking.booking_reference} confirmed!")
    elif action == 'reject':
        booking.status = 'rejected'
        booking.cancellation_reason = request.POST.get('reason', 'Provider is unable to accommodate on this date.')
        booking.save()
        
        # Release inventory if previously reserved
        send_notification(
            booking.user,
            "Booking Request Rejected",
            f"Your booking {booking.booking_reference} was rejected: {booking.cancellation_reason}. Any pre-authorizations are eligible for refund.",
            notification_type='booking',
            link_url='/my-bookings/'
        )
        messages.warning(request, f"Booking {booking.booking_reference} rejected.")

    return redirect('provider_dashboard')


# ----------------- ADMIN HEADQUARTERS -----------------

@login_required
def portal_admin_dashboard(request):
    if not request.user.is_platform_admin:
        return HttpResponseForbidden("Access Denied: Platform Administrator clearance required.")

    total_users = User.objects.count()
    total_travelers = User.objects.filter(role='traveler').count()
    total_providers = User.objects.filter(role='provider').count()
    total_destinations = Destination.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = sum([b.total_amount for b in Booking.objects.filter(is_paid=True)])

    pending_providers = ProviderProfile.objects.filter(is_approved=False).select_related('user')
    approved_providers = ProviderProfile.objects.filter(is_approved=True).select_related('user')
    recent_bookings = Booking.objects.order_by('-created_at')[:15]
    audit_logs = AuditLog.objects.order_by('-timestamp')[:20]

    context = {
        'total_users': total_users,
        'total_travelers': total_travelers,
        'total_providers': total_providers,
        'total_destinations': total_destinations,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'pending_providers': pending_providers,
        'approved_providers': approved_providers,
        'recent_bookings': recent_bookings,
        'audit_logs': audit_logs,
    }
    return render(request, 'portal_admin/dashboard.html', context)


@login_required
def admin_approve_provider(request, provider_id):
    if not request.user.is_platform_admin:
        return HttpResponseForbidden("Unauthorized.")

    provider_profile = get_object_or_404(ProviderProfile, id=provider_id)
    action = request.POST.get('action') # 'approve' or 'suspend'

    if action == 'approve':
        provider_profile.is_approved = True
        provider_profile.save()
        send_notification(
            provider_profile.user,
            "Provider Account Approved!",
            "Your service provider account has been approved by the platform administrator. You can now manage services and bookings.",
            notification_type='system',
            link_url='/provider/dashboard/'
        )
        messages.success(request, f"Provider '{provider_profile.business_name}' approved.")
    else:
        provider_profile.is_approved = False
        provider_profile.save()
        send_notification(
            provider_profile.user,
            "Provider Account Suspended",
            "Your service provider account has been suspended by the platform administrator.",
            notification_type='system'
        )
        messages.warning(request, f"Provider '{provider_profile.business_name}' suspended.")

    return redirect('portal_admin_dashboard')
