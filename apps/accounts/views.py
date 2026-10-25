from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, TravelerProfile, ProviderProfile
from .forms import TravelerRegistrationForm, ProviderRegistrationForm
from apps.notifications.models import send_notification

def traveler_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = TravelerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'traveler'
            user.save()
            
            profile = user.traveler_profile
            profile.travel_style = form.cleaned_data.get('travel_style', 'Family')
            profile.save()

            send_notification(user, "Welcome to AI Smart Tourism!", "Your traveler account is activated. Explore destinations, get AI itineraries, and book experiences.")
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = TravelerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'account_type': 'Traveler'})


def provider_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'provider'
            user.save()

            profile = user.provider_profile
            profile.business_name = form.cleaned_data.get('business_name')
            profile.business_type = form.cleaned_data.get('business_type')
            profile.license_number = form.cleaned_data.get('license_number')
            profile.office_address = form.cleaned_data.get('office_address')
            profile.contact_phone = user.phone
            profile.contact_email = user.email
            profile.is_approved = False # Needs admin approval
            profile.save()

            send_notification(user, "Provider Application Submitted", "Your provider account is under review by administrator. Once approved, you can publish inventory.")
            messages.success(request, "Provider registration submitted! Awaiting administrator approval.")
            return redirect('login')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'account_type': 'Service Provider'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.role == 'provider':
                return redirect('provider_dashboard')
            elif user.role == 'admin':
                return redirect('portal_admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.profile_image = request.POST.get('profile_image', user.profile_image)
        user.save()

        if hasattr(user, 'traveler_profile'):
            tp = user.traveler_profile
            tp.travel_style = request.POST.get('travel_style', tp.travel_style)
            tp.preferred_currency = request.POST.get('preferred_currency', tp.preferred_currency)
            tp.dietary_preferences = request.POST.get('dietary_preferences', tp.dietary_preferences)
            tp.accessibility_needs = request.POST.get('accessibility_needs', tp.accessibility_needs)
            tp.bio = request.POST.get('bio', tp.bio)
            tp.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'user': user})
