import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_tourism.settings')
django.setup()

from decimal import Decimal
from apps.accounts.models import User, TravelerProfile, ProviderProfile
from apps.destinations.models import Destination, TouristAttraction
from apps.bookings.models import Hotel, RoomType, TransportService, Activity

def run_seed():
    print("[Seed] Commencing database seeding for AI Smart Tourism...")

    # 1. Create Default Users (Admin, Provider, Traveler)
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@smarttourism.internal',
            'first_name': 'Platform',
            'last_name': 'Administrator',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()
    print("[Success] Admin account created (User: admin / Pass: admin123)")

    provider_user, _ = User.objects.get_or_create(
        username='provider_goa',
        defaults={
            'email': 'partner@goahospitality.com',
            'first_name': 'Sunil',
            'last_name': 'Fernandes',
            'role': 'provider',
            'phone': '+91 9876543210'
        }
    )
    provider_user.set_password('provider123')
    provider_user.save()
    
    prov_profile, _ = ProviderProfile.objects.get_or_create(
        user=provider_user,
        defaults={
            'business_name': 'Fernandes Coastal Hospitality & Transit',
            'business_type': 'all',
            'license_number': 'GOA-TOUR-2026-9812',
            'contact_phone': '+91 9876543210',
            'is_approved': True,
            'office_address': 'Calangute Main Circle, North Goa'
        }
    )
    prov_profile.is_approved = True
    prov_profile.save()
    print("[Success] Provider account created and approved (User: provider_goa / Pass: provider123)")

    traveler_user, _ = User.objects.get_or_create(
        username='traveler_demo',
        defaults={
            'email': 'traveler@gmail.com',
            'first_name': 'Aarav',
            'last_name': 'Sharma',
            'role': 'traveler',
            'phone': '+91 9123456789'
        }
    )
    traveler_user.set_password('traveler123')
    traveler_user.save()
    print("[Success] Traveler demo account created (User: traveler_demo / Pass: traveler123)")

    # 2. Destinations
    dest_goa, _ = Destination.objects.get_or_create(
        name='Goa',
        defaults={
            'state_country': 'India',
            'tagline': 'Sun, Sand, Heritage Cathedrals & Vibrant Nightlife',
            'description': 'Goa is India’s pocket-sized paradise on the southwest coast, offering a unique blend of Portuguese heritage, golden tropical beaches, lush spice plantations, and historic cathedrals.',
            'cover_image': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('15.498900'),
            'longitude': Decimal('73.827800'),
            'best_time_to_visit': 'October to April',
            'average_budget_per_day': Decimal('4500.00'),
            'is_popular': True
        }
    )

    dest_jaipur, _ = Destination.objects.get_or_create(
        name='Jaipur',
        defaults={
            'state_country': 'Rajasthan, India',
            'tagline': 'The Royal Pink City of Palaces, Forts & Heritage',
            'description': 'Jaipur, the capital of Rajasthan, is known for its regal palaces, ancient hilltop fortresses, colorful textile bazaars, and opulent Rajput hospitality.',
            'cover_image': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('26.912400'),
            'longitude': Decimal('75.787300'),
            'best_time_to_visit': 'November to March',
            'average_budget_per_day': Decimal('3800.00'),
            'is_popular': True
        }
    )

    dest_kerala, _ = Destination.objects.get_or_create(
        name='Kerala Backwaters',
        defaults={
            'state_country': 'Kerala, India',
            'tagline': 'God’s Own Country: Tranquil Lagoons & Lush Greenery',
            'description': 'A serene network of interconnected canals, rivers, and lakes lined with swaying coconut palms, traditional houseboats, and rich Ayurvedic traditions.',
            'cover_image': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('9.498100'),
            'longitude': Decimal('76.338800'),
            'best_time_to_visit': 'September to March',
            'average_budget_per_day': Decimal('4200.00'),
            'is_popular': True
        }
    )

    print("[Success] Destinations seeded (Goa, Jaipur, Kerala)")

    # 3. Tourist Attractions (Outdoor vs Indoor Rain-Friendly)
    # Goa Attractions
    TouristAttraction.objects.get_or_create(
        destination=dest_goa,
        name='Aguada Fort & Lighthouse',
        defaults={
            'category': 'Heritage',
            'description': 'A 17th-century Portuguese fortress overlooking the vast Arabian Sea, featuring an ancient freshwater cistern and iconic lighthouse.',
            'image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('15.492000'),
            'longitude': Decimal('73.773800'),
            'entry_fee': Decimal('50.00'),
            'typical_time_spent_hours': Decimal('2.0'),
            'is_indoor': False,
            'rain_friendly': False,
            'rating': Decimal('4.6')
        }
    )

    TouristAttraction.objects.get_or_create(
        destination=dest_goa,
        name='Calangute & Baga Beachfront',
        defaults={
            'category': 'Nature',
            'description': 'Vibrant coastline famous for gentle waves, watersports, beach shacks, and tropical sunsets.',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('15.544000'),
            'longitude': Decimal('73.755400'),
            'entry_fee': Decimal('0.00'),
            'typical_time_spent_hours': Decimal('3.0'),
            'is_indoor': False,
            'rain_friendly': False,
            'rating': Decimal('4.4')
        }
    )

    TouristAttraction.objects.get_or_create(
        destination=dest_goa,
        name='Museum of Christian Art & Convent',
        defaults={
            'category': 'Museum',
            'description': 'Sheltered indoor gallery housed within the Santa Monica Convent showcasing exquisite Indo-Portuguese sacred relics, sculptures, and art.',
            'image_url': 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('15.503400'),
            'longitude': Decimal('73.911800'),
            'entry_fee': Decimal('150.00'),
            'typical_time_spent_hours': Decimal('2.5'),
            'is_indoor': True,
            'rain_friendly': True,
            'rating': Decimal('4.7')
        }
    )

    TouristAttraction.objects.get_or_create(
        destination=dest_goa,
        name='Basilica of Bom Jesus',
        defaults={
            'category': 'Religious',
            'description': 'UNESCO World Heritage baroque church containing the sacred mortal remains of St. Francis Xavier, featuring ornate covered interiors.',
            'image_url': 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('15.500900'),
            'longitude': Decimal('73.911600'),
            'entry_fee': Decimal('0.00'),
            'typical_time_spent_hours': Decimal('1.5'),
            'is_indoor': True,
            'rain_friendly': True,
            'rating': Decimal('4.8')
        }
    )

    # Jaipur Attractions
    TouristAttraction.objects.get_or_create(
        destination=dest_jaipur,
        name='Amer Fort & Palace Grounds',
        defaults={
            'category': 'Heritage',
            'description': 'Spectacular red sandstone and marble fortress perched atop Cheel ka Teela, renowned for Sheesh Mahal (Mirror Palace) and courtyards.',
            'image_url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('26.985500'),
            'longitude': Decimal('75.851300'),
            'entry_fee': Decimal('200.00'),
            'typical_time_spent_hours': Decimal('3.0'),
            'is_indoor': False,
            'rain_friendly': False,
            'rating': Decimal('4.9')
        }
    )

    TouristAttraction.objects.get_or_create(
        destination=dest_jaipur,
        name='Albert Hall Central Museum',
        defaults={
            'category': 'Museum',
            'description': 'The oldest museum in Rajasthan, modeled on Indo-Saracenic design, housing rare miniature paintings, Persian carpets, Egyptian mummies, and armory.',
            'image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('26.911500'),
            'longitude': Decimal('75.819400'),
            'entry_fee': Decimal('150.00'),
            'typical_time_spent_hours': Decimal('2.5'),
            'is_indoor': True,
            'rain_friendly': True,
            'rating': Decimal('4.8')
        }
    )

    TouristAttraction.objects.get_or_create(
        destination=dest_jaipur,
        name='City Palace Museum & Chandra Mahal',
        defaults={
            'category': 'Heritage',
            'description': 'A sprawling royal palace complex of fusion Rajput-Mughal architecture with covered art galleries, ceremonial halls, and royal costume archives.',
            'image_url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80',
            'latitude': Decimal('26.925800'),
            'longitude': Decimal('75.823700'),
            'entry_fee': Decimal('300.00'),
            'typical_time_spent_hours': Decimal('2.0'),
            'is_indoor': True,
            'rain_friendly': True,
            'rating': Decimal('4.7')
        }
    )

    print("[Success] Attractions seeded with indoor/outdoor weather classifications")

    # 4. Hotels & Rooms
    hotel_goa, _ = Hotel.objects.get_or_create(
        name='Taj Holiday Village & Coastal Resort',
        defaults={
            'provider': provider_user,
            'destination': dest_goa,
            'address': 'Sinquerim, Candolim, North Goa',
            'star_rating': 5,
            'cover_image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80',
            'base_price': Decimal('5500.00'),
            'cancellation_policy': 'Free cancellation up to 24 hours prior to check-in',
            'amenities': 'Beach Access, Infinity Pool, High-Speed WiFi, Spa Center, Oceanfront Breakfast, Airport Transit'
        }
    )

    RoomType.objects.get_or_create(
        hotel=hotel_goa,
        name='Deluxe Ocean Breeze Cottage',
        defaults={
            'description': 'King bed, private garden balcony, sea-facing patio, espresso bar.',
            'capacity_guests': 2,
            'price_per_night': Decimal('5500.00'),
            'total_rooms': 12,
            'available_rooms': 10
        }
    )

    RoomType.objects.get_or_create(
        hotel=hotel_goa,
        name='Presidential Heritage Villa',
        defaults={
            'description': 'Two king master bedrooms, private plunge pool, 24/7 personal butler service.',
            'capacity_guests': 4,
            'price_per_night': Decimal('11500.00'),
            'total_rooms': 4,
            'available_rooms': 3
        }
    )

    hotel_jaipur, _ = Hotel.objects.get_or_create(
        name='Royal Heritage Haveli',
        defaults={
            'provider': provider_user,
            'destination': dest_jaipur,
            'address': 'Khatipura Road, Near Civil Lines, Jaipur',
            'star_rating': 4,
            'cover_image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
            'base_price': Decimal('3800.00'),
            'cancellation_policy': 'Free cancellation up to 48 hours prior to check-in',
            'amenities': 'Courtyard Swimming Pool, Rajasthani Folk Evenings, Marble Suites, Free Breakfast'
        }
    )

    RoomType.objects.get_or_create(
        hotel=hotel_jaipur,
        name='Heritage Deluxe Suite',
        defaults={
            'description': 'Carved teak furniture, marble flooring, frescoed ceiling, modern rain shower.',
            'capacity_guests': 2,
            'price_per_night': Decimal('3800.00'),
            'total_rooms': 15,
            'available_rooms': 14
        }
    )

    print("[Success] Hotels & Room Types created")

    # 5. Transport Services
    TransportService.objects.get_or_create(
        name='Goa Express AC Sleeper Cruiser',
        defaults={
            'provider': provider_user,
            'destination': dest_goa,
            'service_type': 'bus',
            'source_city': 'Hyderabad',
            'destination_city': 'Goa',
            'departure_time': '07:30 PM',
            'estimated_arrival_time': '08:00 AM (+1 Day)',
            'pickup_point': 'Gachibowli Outer Ring Road, Hyderabad',
            'drop_point': 'Panaji Bus Terminal, Goa',
            'price_per_seat': Decimal('1450.00'),
            'total_capacity': 30,
            'available_capacity': 26
        }
    )

    TransportService.objects.get_or_create(
        name='Royal Rajasthan Chauffeur Sedan',
        defaults={
            'provider': provider_user,
            'destination': dest_jaipur,
            'service_type': 'cab',
            'source_city': 'Delhi NCR',
            'destination_city': 'Jaipur',
            'departure_time': '06:00 AM (Flexible on demand)',
            'estimated_arrival_time': '10:30 AM',
            'pickup_point': 'Airport / Hotel Doorstep',
            'drop_point': 'Jaipur City Center',
            'price_per_seat': Decimal('2800.00'),
            'total_capacity': 4,
            'available_capacity': 4
        }
    )

    print("[Success] Transportation schedules created")

    # 6. Activities & Sightseeing
    Activity.objects.get_or_create(
        title='Grand Island Scuba Diving & Dolphin Cruise',
        defaults={
            'provider': provider_user,
            'destination': dest_goa,
            'description': 'Includes PADI-certified instructor dive, underwater video footage, boat cruise past Aguada jail, and buffet lunch on island.',
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80',
            'duration_hours': Decimal('5.0'),
            'time_slot': '07:30 AM - 01:30 PM',
            'price_per_person': Decimal('2200.00'),
            'total_capacity': 25,
            'available_slots': 18
        }
    )

    Activity.objects.get_or_create(
        title='Jaipur Old City Heritage & Street Food Culinary Walk',
        defaults={
            'provider': provider_user,
            'destination': dest_jaipur,
            'description': 'Guided walk through hidden alleys, spice markets, authentic lassi stalls, and historical havelis with an architectural historian.',
            'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
            'duration_hours': Decimal('3.0'),
            'time_slot': '04:00 PM - 07:00 PM',
            'price_per_person': Decimal('850.00'),
            'total_capacity': 15,
            'available_slots': 12
        }
    )

    print("[Success] Activities created")
    print("[Done] Database seeding finished successfully!")

if __name__ == '__main__':
    run_seed()
