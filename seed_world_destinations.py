import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_tourism.settings')
django.setup()

from decimal import Decimal
from apps.accounts.models import User
from apps.destinations.models import Destination, TouristAttraction
from apps.bookings.models import Hotel, RoomType, TransportService, Activity

def seed_world_data():
    print("[Seed] Expanding Destination Catalog with Top Indian & Global World Destinations...")

    # Get or create provider user
    provider = User.objects.filter(role='provider').first()
    if not provider:
        provider = User.objects.filter(is_superuser=True).first()

    # --- 1. DESTINATIONS LIST (India & Worldwide) ---
    destinations_data = [
        # --- Top Indian Destinations ---
        {
            'name': 'Agra',
            'state_country': 'Uttar Pradesh, India',
            'tagline': 'City of the Taj Mahal & Timeless Mughal Majesty',
            'description': 'Agra is world-famous as the home of the iconic Taj Mahal, a UNESCO World Heritage site and monument to love, along with the red sandstone Agra Fort and Fatehpur Sikri.',
            'cover_image': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('27.176700'),
            'longitude': Decimal('78.008100'),
            'best_time_to_visit': 'October to March',
            'average_budget_per_day': Decimal('3200.00'),
            'is_popular': True
        },
        {
            'name': 'Manali',
            'state_country': 'Himachal Pradesh, India',
            'tagline': 'Snow-Capped Himalayan Valleys & Mountain Adventures',
            'description': 'Nestled in the Beas River valley, Manali is a premier Himalayan hill station famous for snow sports at Solang Valley, Rohtang Pass, cedar pine forests, and Tibetan monasteries.',
            'cover_image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('32.243200'),
            'longitude': Decimal('77.189200'),
            'best_time_to_visit': 'October to June',
            'average_budget_per_day': Decimal('3500.00'),
            'is_popular': True
        },
        {
            'name': 'Leh Ladakh',
            'state_country': 'Ladakh, India',
            'tagline': 'The Land of High Passes, Azure Lakes & Monasteries',
            'description': 'Ladakh is a high-altitude desert wonderland renowned for Pangong Tso lake, dramatic moonscapes, high-altitude motorable passes, and ancient Buddhist gompas.',
            'cover_image': 'https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('34.152600'),
            'longitude': Decimal('77.577100'),
            'best_time_to_visit': 'May to September',
            'average_budget_per_day': Decimal('4800.00'),
            'is_popular': True
        },
        {
            'name': 'Varanasi',
            'state_country': 'Uttar Pradesh, India',
            'tagline': 'Spiritual Heart of India on the Sacred River Ganges',
            'description': 'One of the world’s oldest continuously inhabited cities, famous for its riverfront ghats, mystical evening Ganga Aarti rituals, ancient silk weaving, and spiritual heritage.',
            'cover_image': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('25.317600'),
            'longitude': Decimal('82.973900'),
            'best_time_to_visit': 'October to March',
            'average_budget_per_day': Decimal('2600.00'),
            'is_popular': True
        },
        {
            'name': 'Udaipur',
            'state_country': 'Rajasthan, India',
            'tagline': 'The Romantic City of Lakes & Marble Palaces',
            'description': 'Known as the Venice of the East, Udaipur is crowned by the majestic City Palace on Lake Pichola, tranquil boat rides, vintage car museums, and Rajput architecture.',
            'cover_image': 'https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('24.585400'),
            'longitude': Decimal('73.712500'),
            'best_time_to_visit': 'October to March',
            'average_budget_per_day': Decimal('4200.00'),
            'is_popular': True
        },
        {
            'name': 'Munnar',
            'state_country': 'Kerala, India',
            'tagline': 'Emerald Tea Plantations & Misty Western Ghats',
            'description': 'A picturesque hill station in the Western Ghats surrounded by rolling tea garden hills, waterfalls, misty peaks, and the endangered Nilgiri Tahr at Eravikulam.',
            'cover_image': 'https://images.unsplash.com/photo-1596401057633-54a8fe8ef647?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('10.088900'),
            'longitude': Decimal('77.059500'),
            'best_time_to_visit': 'September to April',
            'average_budget_per_day': Decimal('3400.00'),
            'is_popular': True
        },
        {
            'name': 'Darjeeling',
            'state_country': 'West Bengal, India',
            'tagline': 'Queen of the Hills, Himalayan Toy Train & World Tea',
            'description': 'Perched with views of Mount Kanchenjunga, Darjeeling is renowned for UNESCO heritage Himalayan Railway toy trains, colonial cottages, and aromatic tea estates.',
            'cover_image': 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('27.041000'),
            'longitude': Decimal('88.266300'),
            'best_time_to_visit': 'March to May, Oct to Dec',
            'average_budget_per_day': Decimal('3100.00'),
            'is_popular': True
        },
        {
            'name': 'Amritsar',
            'state_country': 'Punjab, India',
            'tagline': 'Sacred Golden Temple & Historic Patriotic Heritage',
            'description': 'Home to the resplendent Harmandir Sahib (Golden Temple), the historic Jallianwala Bagh memorial, Wagah Border retreat ceremony, and mouth-watering Punjabi kulchas.',
            'cover_image': 'https://images.unsplash.com/photo-1583321500900-82807e458f3c?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('31.634000'),
            'longitude': Decimal('74.872300'),
            'best_time_to_visit': 'October to March',
            'average_budget_per_day': Decimal('2800.00'),
            'is_popular': True
        },
        {
            'name': 'Andaman Islands',
            'state_country': 'Andaman & Nicobar, India',
            'tagline': 'Turquoise Waters, Coral Reefs & White Sand Shores',
            'description': 'An idyllic tropical archipelago in the Bay of Bengal, featuring Radhanagar Beach on Havelock Island, scuba diving, bioluminescence, and historic Cellular Jail.',
            'cover_image': 'https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('11.976100'),
            'longitude': Decimal('92.987600'),
            'best_time_to_visit': 'October to May',
            'average_budget_per_day': Decimal('5200.00'),
            'is_popular': True
        },

        # --- Top Global / International Destinations ---
        {
            'name': 'Paris',
            'state_country': 'France',
            'tagline': 'City of Light, Haute Couture, Art & Culinary Grandeur',
            'description': 'The French capital is an epicenter of global culture, featuring the Eiffel Tower, the Louvre Museum, charming sidewalk bistros, Montmartre, and the Seine River.',
            'cover_image': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('48.856600'),
            'longitude': Decimal('2.352200'),
            'best_time_to_visit': 'April to October',
            'average_budget_per_day': Decimal('14500.00'),
            'is_popular': True
        },
        {
            'name': 'Dubai',
            'state_country': 'United Arab Emirates',
            'tagline': 'Futuristic Skylines, Luxury Shopping & Desert Dunes',
            'description': 'A dazzling metropolis in the UAE famed for the sky-piercing Burj Khalifa, Palm Jumeirah archipelago, glamorous mega-malls, and exhilarating desert safaris.',
            'cover_image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('25.204800'),
            'longitude': Decimal('55.270800'),
            'best_time_to_visit': 'November to March',
            'average_budget_per_day': Decimal('13500.00'),
            'is_popular': True
        },
        {
            'name': 'Tokyo',
            'state_country': 'Japan',
            'tagline': 'High-Tech Futurism Meets Ancient Shinto Traditions',
            'description': 'Japan’s dynamic capital blends neon-lit skyscrapers with centuries-old temples, world-class sushi dining, anime culture in Akihabara, and peaceful Meiji shrines.',
            'cover_image': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('35.676200'),
            'longitude': Decimal('139.650300'),
            'best_time_to_visit': 'March to May, Sept to Nov',
            'average_budget_per_day': Decimal('12800.00'),
            'is_popular': True
        },
        {
            'name': 'Bali',
            'state_country': 'Indonesia',
            'tagline': 'Island of the Gods: Volcanic Peaks, Surfing & Temples',
            'description': 'Indonesia’s most famous island paradise, famed for its forested volcanic mountains, iconic rice paddy terraces in Ubud, vibrant coral reefs, and cliffside temples.',
            'cover_image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('-8.340500'),
            'longitude': Decimal('115.092000'),
            'best_time_to_visit': 'April to October',
            'average_budget_per_day': Decimal('5500.00'),
            'is_popular': True
        },
        {
            'name': 'Rome',
            'state_country': 'Italy',
            'tagline': 'The Eternal City of Colosseum, Vatican & Gelato',
            'description': 'Steeped in nearly 3,000 years of globally influential history, art, and architecture, featuring the Colosseum, the Pantheon, St. Peter’s Basilica, and lively piazzas.',
            'cover_image': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('41.902800'),
            'longitude': Decimal('12.496400'),
            'best_time_to_visit': 'April to June, Sept to Oct',
            'average_budget_per_day': Decimal('13800.00'),
            'is_popular': True
        },
        {
            'name': 'London',
            'state_country': 'United Kingdom',
            'tagline': 'Royal Palaces, West End Theatres & Historic River Thames',
            'description': 'A world cultural hub with iconic Big Ben, Tower Bridge, British Museum, world-renowned West End shows, red double-decker buses, and sprawling royal parks.',
            'cover_image': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('51.507400'),
            'longitude': Decimal('-0.127800'),
            'best_time_to_visit': 'May to September',
            'average_budget_per_day': Decimal('15000.00'),
            'is_popular': True
        },
        {
            'name': 'New York City',
            'state_country': 'United States',
            'tagline': 'The City That Never Sleeps: Broadway, Skyline & Parks',
            'description': 'Comprising 5 boroughs sitting where the Hudson River meets the Atlantic Ocean, with Central Park, Times Square, Broadway, and soaring skyscrapers.',
            'cover_image': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('40.712800'),
            'longitude': Decimal('-74.006000'),
            'best_time_to_visit': 'April to June, Sept to Nov',
            'average_budget_per_day': Decimal('18000.00'),
            'is_popular': True
        },
        {
            'name': 'Maldives',
            'state_country': 'Maldives',
            'tagline': 'Private Overwater Bungalows & Crystal Coral Lagoons',
            'description': 'A tropical nation in the Indian Ocean composed of 26 ring-shaped atolls, celebrated for pristine turquoise waters, private sandbanks, and marine wildlife.',
            'cover_image': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('3.202800'),
            'longitude': Decimal('73.220700'),
            'best_time_to_visit': 'November to April',
            'average_budget_per_day': Decimal('19500.00'),
            'is_popular': True
        },
        {
            'name': 'Singapore',
            'state_country': 'Singapore',
            'tagline': 'Garden City of Futuristic Supertrees & Culinary Street Food',
            'description': 'An island city-state off southern Malaysia featuring Gardens by the Bay, Marina Bay Sands infinity pool, Michelin-starred hawker centers, and Sentosa island.',
            'cover_image': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('1.352100'),
            'longitude': Decimal('103.819800'),
            'best_time_to_visit': 'November to January, June to Aug',
            'average_budget_per_day': Decimal('11500.00'),
            'is_popular': True
        },
        {
            'name': 'Bangkok',
            'state_country': 'Thailand',
            'tagline': 'Grand Ornate Shrines, Floating Markets & Vibrant Street Life',
            'description': 'Thailand’s bustling capital known for ornate shrines like Wat Arun, the Grand Palace, bustling floating markets, tuk-tuks, and vibrant night bazaars.',
            'cover_image': 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('13.756300'),
            'longitude': Decimal('100.501800'),
            'best_time_to_visit': 'November to February',
            'average_budget_per_day': Decimal('4800.00'),
            'is_popular': True
        },
        {
            'name': 'Swiss Alps & Zurich',
            'state_country': 'Switzerland',
            'tagline': 'Majestic Glaciers, Pristine Alpine Lakes & Scenic Trains',
            'description': 'Breathtaking alpine scenery featuring the Jungfraujoch summit, Lake Zurich, cogwheel mountain trains, Swiss chocolate houses, and world-class ski slopes.',
            'cover_image': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('47.376900'),
            'longitude': Decimal('8.541700'),
            'best_time_to_visit': 'June to September, Dec to March',
            'average_budget_per_day': Decimal('19000.00'),
            'is_popular': True
        },
        {
            'name': 'Sydney',
            'state_country': 'Australia',
            'tagline': 'Harbour Opera House, Golden Surf Beaches & Blue Mountains',
            'description': 'Australia’s iconic harbour city famed for the sail-designed Sydney Opera House, Harbour Bridge climb, Bondi Beach surfing, and scenic coastal trails.',
            'cover_image': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=1200&q=80',
            'latitude': Decimal('-33.868800'),
            'longitude': Decimal('151.209300'),
            'best_time_to_visit': 'September to November, March to May',
            'average_budget_per_day': Decimal('14000.00'),
            'is_popular': True
        }
    ]

    dest_objs = {}
    for d in destinations_data:
        dest_obj, _ = Destination.objects.update_or_create(
            name=d['name'],
            defaults=d
        )
        dest_objs[d['name']] = dest_obj

    print(f"[Done] Seeded {len(dest_objs)} World & Indian Destinations.")

    # --- 2. MULTIPLE ACTIVITIES FOR EVERY DESTINATION ---
    # Each place gets 3 to 4 distinct bookable activities & guided experiences!
    activities_data = [
        # Agra
        ('Taj Mahal Sunrise Guided Tour with Historian', 'Agra', 'Beat the heat and crowds with an early morning VIP entry guided by an archaeological historian.', 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80', 3.0, '05:30 AM - 08:30 AM', 1200.00, 25),
        ('Agra Fort & Mehtab Bagh Sunset Heritage Walk', 'Agra', 'Explore the massive red sandstone Mughal stronghold and watch the Taj Mahal glow across the Yamuna River.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 3.5, '03:30 PM - 07:00 PM', 950.00, 20),
        ('Mughlai Cooking Masterclass & Street Food Tour', 'Agra', 'Discover ancient culinary recipes of Mughal emperors, including authentic Agra petha and tandoori delicacies.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 2.5, '06:00 PM - 08:30 PM', 800.00, 15),

        # Manali
        ('Solang Valley Tandem Paragliding & Zipline Pass', 'Manali', 'Soar over pine-clad Himalayan valleys with experienced pilots, followed by the high-wire zipline course.', 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80', 3.0, '09:00 AM - 12:00 PM', 2400.00, 20),
        ('Rohtang Pass Snowmobile & Skiing Expedition', 'Manali', 'High-altitude snow adventure at 3,978 meters with roundtrip transport, snow suits, and ski coaching.', 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80', 6.0, '07:00 AM - 01:00 PM', 3200.00, 15),
        ('Old Manali Pine Forest & Apple Orchard Nature Trail', 'Manali', 'Guided walking tour through historic cedar groves, wooden temples, and local artisan woolen craft sheds.', 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80', 2.5, '03:00 PM - 05:30 PM', 650.00, 25),

        # Paris
        ('Louvre Museum Priority Guided Masterpiece Tour', 'Paris', 'Skip the lines to view the Mona Lisa, Venus de Milo, and Winged Victory with an art historian.', 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80', 3.0, '10:00 AM - 01:00 PM', 4800.00, 20),
        ('Eiffel Tower Summit Access & Seine River Cruise', 'Paris', 'Ascend to the top of the Eiffel Tower, followed by a panoramic glass-canopy boat cruise along the Seine.', 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80', 4.0, '04:00 PM - 08:00 PM', 5500.00, 30),
        ('Montmartre Walking Food Tour & French Pastry Tasting', 'Paris', 'Stroll through cobblestone streets to taste artisanal cheeses, macarons, freshly baked baguettes, and wines.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.0, '02:00 PM - 05:00 PM', 3900.00, 15),

        # Dubai
        ('Premium Desert Safari with Dune Bashing & BBQ', 'Dubai', '4x4 dune bashing, sandboarding, camel rides, falconry show, and a 5-star Arabian barbecue under the stars.', 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80', 6.0, '03:30 PM - 09:30 PM', 3800.00, 40),
        ('Burj Khalifa 124th & 125th Floor Sky Deck Pass', 'Dubai', 'Travel up the world’s fastest double-deck elevator to witness panoramic 360-degree views of the Persian Gulf.', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', 2.0, '11:00 AM - 01:00 PM', 3200.00, 50),
        ('Dubai Marina Luxury Shared Yacht Cruise with Buffet', 'Dubai', 'Cruise past Ain Dubai and the Palm Jumeirah on an opulent yacht with onboard gourmet refreshments.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 3.0, '05:00 PM - 08:00 PM', 4500.00, 25),

        # Tokyo
        ('Mount Fuji & Lake Kawaguchi Scenic Day Tour', 'Tokyo', 'Full-day tour from Tokyo to Mount Fuji 5th Station, Oshino Hakkai springs, and a panoramic lake ropeway.', 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=800&q=80', 8.0, '08:00 AM - 04:00 PM', 6500.00, 30),
        ('Shinjuku & Shibuya Neon Night Street Food Crawl', 'Tokyo', 'Taste yakitori skewers, authentic gyoza, and matcha treats through vibrant hidden Omoide Yokocho alleys.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.5, '06:00 PM - 09:30 PM', 4200.00, 15),
        ('Akihabara Tech & Anime Culture Walking Tour', 'Tokyo', 'Guided dive into gaming arcades, maid cafes, manga shops, and retro collectible centers.', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80', 2.5, '01:30 PM - 04:00 PM', 2800.00, 20),

        # Bali
        ('Ubud Jungle Swing, Rice Terraces & Waterfall Tour', 'Bali', 'Soar over tropical valleys on the famous giant swing, walk Tegalalang terraces, and swim in Tegenungan falls.', 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80', 6.0, '08:30 AM - 02:30 PM', 2200.00, 30),
        ('Mount Batur Sunrise Trek with Volcanic Breakfast', 'Bali', 'Early morning hike to the active caldera summit to witness breathtaking sunrise above the clouds.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 5.0, '03:30 AM - 08:30 AM', 2800.00, 20),
        ('Nusa Penida Island Speedboat Day Cruise & Snorkel', 'Bali', 'Speedboat excursion to Kelingking T-Rex cliff, Angel’s Billabong, and snorkeling with giant manta rays.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 7.0, '07:00 AM - 02:00 PM', 3400.00, 25),

        # Rome
        ('Colosseum, Roman Forum & Palatine Hill Skip-the-Line', 'Rome', 'Step into the arena floor where gladiators fought and explore the ruins of imperial Roman emperors.', 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80', 3.0, '09:30 AM - 12:30 PM', 4200.00, 25),
        ('Vatican Museums, Sistine Chapel & St. Peter’s Tour', 'Rome', 'Marvel at Michelangelo’s ceiling frescoes, the Gallery of Maps, and St. Peter’s Basilica with VIP entry.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 3.5, '01:30 PM - 05:00 PM', 4900.00, 20),
        ('Trastevere Twilight Food, Wine & Gelato Walking Tour', 'Rome', 'Savor authentic carbonara, crispy supplì, cured prosciutto, and creamy Roman gelato in historic alleys.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.0, '06:00 PM - 09:00 PM', 3500.00, 15),

        # London
        ('Tower of London & Crown Jewels Official Tour', 'London', 'Discover centuries of royal intrigue, meet the Yeoman Warders (Beefeaters), and see the sparkling Crown Jewels.', 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80', 3.0, '10:00 AM - 01:00 PM', 3600.00, 30),
        ('London Eye Flight & River Thames Panoramic Cruise', 'London', 'Take in 360-degree skyline views of Westminster from your climate-controlled pod and a scenic cruise.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 2.5, '02:00 PM - 04:30 PM', 3200.00, 40),
        ('Historic British Pubs & Literary Soho Evening Crawl', 'London', 'Visit historic taverns frequented by Charles Dickens and George Orwell while tasting British craft ales.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.0, '06:30 PM - 09:30 PM', 2800.00, 18),

        # New York City
        ('Statue of Liberty & Ellis Island Guided Cruise', 'New York City', 'Roundtrip ferry to Liberty Island, monument grounds access, and Ellis Island National Museum of Immigration.', 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800&q=80', 4.0, '09:00 AM - 01:00 PM', 3900.00, 35),
        ('Empire State Building 86th Floor Observatory Pass', 'New York City', 'Experience world-famous panoramic vistas of Manhattan and beyond from the art-deco observation deck.', 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80', 2.0, '05:00 PM - 07:00 PM', 3500.00, 50),
        ('Central Park Guided Bike Tour & Hidden Film Locations', 'New York City', 'Pedal past Bethesda Fountain, Strawberry Fields, and Bow Bridge with an entertaining NYC film guide.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 2.5, '02:00 PM - 04:30 PM', 2600.00, 20),

        # Maldives
        ('Catamaran Snorkeling with Manta Rays & Sea Turtles', 'Maldives', 'Guided boat excursion to protected coral atolls to swim alongside gentle manta rays and sea turtles.', 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80', 4.0, '09:00 AM - 01:00 PM', 4500.00, 16),
        ('Private Sandbank Picnic with Drone Aerial Photography', 'Maldives', 'Speedboat ride to an uninhabited white sandbar surrounded by turquoise water with a gourmet picnic.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 3.5, '01:30 PM - 05:00 PM', 6500.00, 10),
        ('Sunset Dolphin Cruise with Tropical Mocktails', 'Maldives', 'Scenic wooden dhoni cruise at golden hour into channels where pods of spinner dolphins leap alongside.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 2.0, '05:30 PM - 07:30 PM', 3200.00, 25),

        # Singapore
        ('Gardens by the Bay & Cloud Forest Supertree Pass', 'Singapore', 'Explore the world’s largest glass greenhouse with indoor mountain waterfall and Supertree skyway walk.', 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=800&q=80', 3.5, '10:00 AM - 01:30 PM', 2800.00, 40),
        ('Marina Bay Sands SkyPark & Night Light Show Cruise', 'Singapore', 'Admire Singapore from 57 floors high, followed by a bumboat river cruise past the Spectra water show.', 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80', 3.0, '06:00 PM - 09:00 PM', 3400.00, 30),
        ('Chinatown & Katong Peranakan Hawker Food Safari', 'Singapore', 'Taste Michelin-lauded chicken rice, spicy laksa noodles, satay, and pandan chiffon cakes.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.0, '02:00 PM - 05:00 PM', 2600.00, 15),

        # Bangkok
        ('Damnoen Saduak Floating Market & Maeklong Train Market', 'Bangkok', 'Experience paddle-boat shopping along historic canals and see market stalls swiftly retract for passing trains.', 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=800&q=80', 6.0, '07:30 AM - 01:30 PM', 2200.00, 25),
        ('Grand Palace & Wat Pho Giant Reclining Buddha Tour', 'Bangkok', 'Discover Thailand’s sacred royal palace compound and the 46-meter-long gold-leaf reclining Buddha.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 3.5, '09:00 AM - 12:30 PM', 1900.00, 30),
        ('Chao Phraya Princess Luxury Dinner Buffet Cruise', 'Bangkok', 'Glide past illuminated temples Wat Arun and Grand Palace while enjoying a Thai-international dinner with live band.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 2.5, '07:00 PM - 09:30 PM', 2600.00, 40),

        # Swiss Alps & Zurich
        ('Jungfraujoch Top of Europe High-Alpine Train Expedition', 'Swiss Alps & Zurich', 'Cogwheel train ascent to Europe’s highest railway station at 3,454m, featuring the Ice Palace and Aletsch Glacier.', 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=800&q=80', 9.0, '07:30 AM - 04:30 PM', 8500.00, 25),
        ('Mount Titlis Revolving Cable Car & Cliff Walk', 'Swiss Alps & Zurich', 'Ride the world’s first rotating cable car to permanent snow fields and cross Europe’s highest suspension bridge.', 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80', 6.0, '09:00 AM - 03:00 PM', 6800.00, 30),
        ('Lake Zurich Scenic Boat Cruise & Swiss Fondue Tasting', 'Swiss Alps & Zurich', 'Relax on a lake cruiser with vineyard views, followed by an authentic Swiss cheese fondue dining session.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 3.0, '05:00 PM - 08:00 PM', 4900.00, 20),

        # Sydney
        ('Sydney Opera House Behind-the-Scenes Architectural Tour', 'Sydney', 'Exclusive guided access through the world-famous concert halls and theatres designed by Jørn Utzon.', 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800&q=80', 2.0, '10:30 AM - 12:30 PM', 3200.00, 30),
        ('Blue Mountains & Scenic World Railway Day Trip', 'Sydney', 'Explore the Three Sisters rock formation, ride the world’s steepest railway, and see native kangaroos.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 8.0, '08:00 AM - 04:00 PM', 5800.00, 25),
        ('Bondi to Coogee Coastal Walk & Surf Taster Session', 'Sydney', 'Breathtaking ocean clifftop walk followed by beginner surfing coaching on golden Bondi Beach sands.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.5, '02:00 PM - 05:30 PM', 3600.00, 20),

        # Leh Ladakh
        ('Pangong Tso Lake & Chang La Pass Day Expedition', 'Leh Ladakh', 'Cross the world’s 3rd highest pass to marvel at the color-changing blue waters of Pangong Lake.', 'https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80', 9.0, '06:30 AM - 03:30 PM', 3800.00, 18),
        ('Nubra Valley & Hunder Double-Humped Camel Safari', 'Leh Ladakh', 'Ride Bactrian double-humped camels through high-altitude white sand dunes backed by snowy peaks.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 5.0, '01:00 PM - 06:00 PM', 2600.00, 20),
        ('Thiksey & Hemis Monasteries Spiritual Trail', 'Leh Ladakh', 'Witness morning Buddhist chanting rituals, colossal Maitreya Buddha statues, and ancient silk thangkas.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 4.0, '08:00 AM - 12:00 PM', 1400.00, 25),

        # Varanasi
        ('Dawn Boat Ride on Sacred Ganges & Morning Rituals', 'Varanasi', 'Row silently past cremation ghats and bathing pilgrims as the sun rises over the riverfront.', 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80', 2.5, '05:30 AM - 08:00 AM', 800.00, 30),
        ('Dashashwamedh Ghat Evening Ganga Aarti VIP Seating', 'Varanasi', 'Reserved terrace seats to witness the rhythmic brass lamp chanting ceremony honoring mother Ganga.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 2.0, '06:00 PM - 08:00 PM', 650.00, 25),
        ('Sarnath Buddhist Cradle & Ancient Stupa Tour', 'Varanasi', 'Visit the Deer Park where Lord Buddha delivered his first sermon after enlightenment and the Ashoka Pillar.', 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80', 3.5, '01:30 PM - 05:00 PM', 900.00, 20),

        # Udaipur
        ('Lake Pichola Royal Sunset Boat Cruise to Jag Mandir', 'Udaipur', 'Private boat cruise reflecting shimmering marble palaces at sunset, with entry to island gardens.', 'https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=800&q=80', 2.5, '04:30 PM - 07:00 PM', 1400.00, 25),
        ('City Palace Complex Guided Tour & Vintage Car Gallery', 'Udaipur', 'Explore Mewar royal suites, peacock courtyards, and the royal family’s classic Rolls Royce collection.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 3.5, '10:00 AM - 01:30 PM', 1200.00, 30),
        ('Bagore Ki Haveli Rajasthani Puppet & Dharohar Dance', 'Udaipur', 'Evening cultural theatre featuring Chari dance, fire acts, and master Rajasthani puppeteers.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 2.0, '06:30 PM - 08:30 PM', 750.00, 40),

        # Goa (Extra exciting activities)
        ('Grand Island Scuba Diving & Dolphin Cruise', 'Goa', 'Includes PADI-certified instructor dive, underwater video footage, boat cruise past Aguada jail, and buffet lunch on island.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 5.0, '07:30 AM - 01:30 PM', 2200.00, 25),
        ('North Goa Baga Watersports Combo (Parasailing, Jet Ski, Banana Ride)', 'Goa', 'All-in-one adrenaline pass featuring parasailing with ocean dip, jet ski speed runs, and bumper rides.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 3.0, '10:00 AM - 01:00 PM', 1850.00, 35),
        ('Mandovi River Luxury Sunset Catamaran with Live DJ', 'Goa', 'Cruising under Mandovi bridges with panoramic sunset vistas, complimentary drinks, and Goan folk beats.', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', 2.5, '05:30 PM - 08:00 PM', 1100.00, 40),

        # Jaipur (Extra exciting activities)
        ('Jaipur Old City Heritage & Street Food Culinary Walk', 'Jaipur', 'Guided walk through hidden alleys, spice markets, authentic lassi stalls, and historical havelis with an architectural historian.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 3.0, '04:00 PM - 07:00 PM', 850.00, 20),
        ('Amer Fort Sunrise Royal Jeep Safari & Elephant Care Experience', 'Jaipur', 'Open 4x4 jeep safari around the Aravalli moat, followed by feeding and walking elephants at an ethical sanctuary.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 3.5, '06:00 AM - 09:30 AM', 1950.00, 15),
        ('Nahargarh Fort Sunset Mountain Cycling Expedition', 'Jaipur', 'Guided cycling tour ascending through Nahargarh sanctuary trails to catch golden sunset over the Pink City.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 3.0, '04:30 PM - 07:30 PM', 1350.00, 18),
    ]

    act_count = 0
    for title, dest_name, desc, img, hours, slot, price, cap in activities_data:
        dest_obj = dest_objs.get(dest_name) or Destination.objects.filter(name__icontains=dest_name).first()
        if dest_obj and provider:
            Activity.objects.update_or_create(
                title=title,
                destination=dest_obj,
                defaults={
                    'provider': provider,
                    'description': desc,
                    'image_url': img,
                    'duration_hours': Decimal(str(hours)),
                    'time_slot': slot,
                    'price_per_person': Decimal(str(price)),
                    'total_capacity': cap,
                    'available_slots': cap - 3,
                    'is_active': True
                }
            )
            act_count += 1

    print(f"[Done] Seeded {act_count} unique Activities across all destinations.")

    # --- 3. ATTRACTIONS FOR NEW DESTINATIONS ---
    # Give every new destination key indoor and outdoor attractions
    new_attractions = [
        # Agra
        ('Taj Mahal Monument', 'Agra', 'Heritage', 'Ivory-white marble mausoleum on the right bank of river Yamuna, universally admired UNESCO world treasure.', 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80', 27.1751, 78.0421, 250.00, 3.0, False, False, 5.0),
        ('Agra Fort Imperial Palace', 'Agra', 'Heritage', '16th-century Mughal monument known as the Red Fort of Agra, with royal courtyards and marble pavilions.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 27.1795, 78.0211, 150.00, 2.5, True, True, 4.8),
        ('Fatehpur Sikri Royal City', 'Agra', 'Heritage', 'Magnificent fortified ghost city built by Emperor Akbar featuring Buland Darwaza.', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80', 27.0945, 77.6679, 100.00, 2.5, False, True, 4.7),

        # Manali
        ('Solang Valley Mountain Pass', 'Manali', 'Adventure', 'Alpine valley offering paragliding, zorbing, quad biking, and winter ski slopes.', 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80', 32.3166, 77.1572, 100.00, 3.5, False, False, 4.8),
        ('Hadimba Devi Forest Temple', 'Manali', 'Heritage', 'Ancient wooden pagoda temple built in 1553 surrounded by towering deodar pine forest.', 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80', 32.2483, 77.1812, 50.00, 1.5, True, True, 4.7),
        ('Rohtang Snow Crest', 'Manali', 'Nature', 'Iconic Himalayan pass with breathtaking views of glaciers, peaks, and Lahaul valley.', 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80', 32.3716, 77.2466, 200.00, 4.0, False, False, 4.9),

        # Paris
        ('Eiffel Tower', 'Paris', 'Heritage', 'Wrought-iron lattice tower on the Champ de Mars, the defining symbol of Paris.', 'https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?auto=format&fit=crop&w=800&q=80', 48.8584, 2.2945, 2500.00, 2.5, False, False, 4.9),
        ('Louvre Museum & Glass Pyramid', 'Paris', 'Museum', 'The world’s most-visited art museum, home to the Mona Lisa and French crown jewels.', 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80', 48.8606, 2.3376, 1800.00, 3.5, True, True, 5.0),
        ('Arc de Triomphe & Champs-Élysées', 'Paris', 'Heritage', 'Honours those who fought for France, offering a high rooftop view over 12 grand avenues.', 'https://images.unsplash.com/photo-1509299349698-dd22323b5963?auto=format&fit=crop&w=800&q=80', 48.8738, 2.2950, 1200.00, 2.0, False, True, 4.8),

        # Dubai
        ('Burj Khalifa Observation Deck', 'Dubai', 'Heritage', 'The tallest building and freestanding structure in the world, standing at 828 meters.', 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80', 25.1972, 55.2744, 3400.00, 2.0, True, True, 4.9),
        ('Dubai Mall & Underwater Aquarium', 'Dubai', 'Shopping', 'World’s premier entertainment destination featuring an indoor shark tunnel and Olympic ice rink.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 25.1985, 55.2796, 1500.00, 3.0, True, True, 4.8),
        ('Palm Jumeirah & Atlantis Aquaventure', 'Dubai', 'Adventure', 'Iconic palm-tree shaped artificial island featuring record-breaking water slides and private beaches.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 25.1304, 55.1171, 3800.00, 4.0, False, False, 4.8),

        # Tokyo
        ('Senso-ji Ancient Temple', 'Tokyo', 'Religious', 'Tokyo’s oldest Buddhist temple founded in 645 AD, approached via the bustling Nakamise shopping street.', 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=800&q=80', 35.7148, 139.7967, 0.00, 2.0, False, True, 4.8),
        ('Tokyo Skytree Panoramic Tower', 'Tokyo', 'Heritage', 'Soaring 634-meter broadcast tower with glass floors and sweeping panoramic views across Tokyo Bay.', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80', 35.7101, 139.8107, 1800.00, 2.5, True, True, 4.7),
        ('Shibuya Crossing & Hachiko Plaza', 'Tokyo', 'Relaxation', 'The world’s busiest pedestrian intersection, surrounded by dazzling giant screens and energy.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 35.6595, 139.7005, 0.00, 1.5, False, True, 4.8),

        # Bali
        ('Tanah Lot Sea Temple', 'Bali', 'Religious', 'Ancient Hindu pilgrimage temple perched on an offshore rock formation amidst crashing waves.', 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80', -8.6212, 115.0868, 300.00, 2.0, False, False, 4.7),
        ('Ubud Sacred Monkey Forest Sanctuary', 'Bali', 'Nature', 'Lush tropical forest sanctuary home to over 1,000 Balinese long-tailed monkeys and mossy temples.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', -8.5194, 115.2606, 400.00, 2.5, False, False, 4.6),
        ('Uluwatu Cliffside Temple & Kecak Dance', 'Bali', 'Heritage', 'Majestic clifftop temple perched 70 meters above the Indian Ocean, famous for evening fire dance shows.', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', -8.8291, 115.0849, 450.00, 2.5, False, False, 4.9),

        # Rome
        ('The Colosseum Arena', 'Rome', 'Heritage', 'The largest ancient amphitheatre ever built, hosting gladiatorial contests and public spectacles in 80 AD.', 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80', 41.8902, 12.4922, 1600.00, 2.5, False, True, 4.9),
        ('Vatican Museums & Sistine Chapel', 'Rome', 'Museum', 'Home to the Roman Catholic Church’s immense art collection and Michelangelo’s ceiling masterpiece.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 41.9065, 12.4536, 1900.00, 3.5, True, True, 5.0),
        ('Trevi Fountain & Spanish Steps', 'Rome', 'Relaxation', 'Spectacular 18th-century baroque fountain where tossing a coin guarantees your return to Rome.', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80', 41.9009, 12.4833, 0.00, 1.5, False, True, 4.8),

        # London
        ('Big Ben & Palace of Westminster', 'London', 'Heritage', 'The iconic Elizabeth Tower clock and seat of the UK Parliament on the banks of the River Thames.', 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80', 51.5007, -0.1246, 0.00, 1.5, False, True, 4.8),
        ('British Museum of World Antiquities', 'London', 'Museum', 'World-famous museum dedicated to human history, art, and culture, housing the Rosetta Stone.', 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80', 51.5194, -0.1270, 0.00, 3.0, True, True, 4.9),
        ('The London Eye River Wheel', 'London', 'Relaxation', 'Cantilevered observation wheel on the South Bank providing unmatched 360-degree capital vistas.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 51.5033, -0.1195, 2800.00, 1.5, True, True, 4.7),

        # New York City
        ('Statue of Liberty & Ellis Island', 'New York City', 'Heritage', 'A colossal neoclassical sculpture on Liberty Island gifted by France, welcoming millions of arrivals.', 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800&q=80', 40.6892, -74.0445, 2200.00, 3.5, False, True, 4.9),
        ('Central Park Pathways & Bow Bridge', 'New York City', 'Nature', '843-acre urban oasis in the heart of Manhattan featuring lakes, strawberry fields, and woodlands.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 40.7829, -73.9654, 0.00, 2.5, False, False, 4.8),
        ('Metropolitan Museum of Art (The Met)', 'New York City', 'Museum', 'One of the world’s largest art galleries with over two million works spanning 5,000 years.', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80', 40.7794, -73.9632, 2500.00, 3.5, True, True, 4.9),

        # Maldives
        ('Baa Atoll Biosphere Reserve Reef', 'Maldives', 'Nature', 'UNESCO Biosphere reserve famous for world-class snorkeling with whale sharks and manta rays.', 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80', 5.1333, 72.9667, 3500.00, 4.0, False, False, 5.0),
        ('Male Friday Mosque & Heritage Center', 'Maldives', 'Religious', '17th-century coral stone mosque carved with intricate Quranic scripts and lacquer woodwork.', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80', 4.1773, 73.5133, 0.00, 1.5, True, True, 4.6),
        ('Maafushi Water Lagoon & Sandbar', 'Maldives', 'Relaxation', 'Picturesque powder-white sandbank surrounded by iridescent turquoise water, perfect for drone photos.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80', 3.9416, 73.4897, 1200.00, 2.5, False, False, 4.8),

        # Singapore
        ('Gardens by the Bay & Flower Dome', 'Singapore', 'Nature', 'Futuristic nature park featuring vertical Supertree gardens and misty cloud forest conservatory.', 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=800&q=80', 1.2816, 103.8636, 2200.00, 3.0, True, True, 4.9),
        ('Marina Bay Sands SkyPark Observation Deck', 'Singapore', 'Heritage', 'Iconic ship-shaped rooftop offering 360-degree vistas of Singapore’s skyline and the shipping straits.', 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80', 1.2834, 103.8607, 2400.00, 2.0, False, True, 4.8),
        ('Sentosa Island & Universal Studios', 'Singapore', 'Adventure', 'Island resort destination with sandy beaches, oceanarium, and thrilling theme park rides.', 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80', 1.2494, 103.8303, 3500.00, 4.5, False, True, 4.8),
    ]

    for name, dest_name, cat, desc, img, lat, lng, fee, hours, indoor, rain, rating in new_attractions:
        dest_obj = dest_objs.get(dest_name) or Destination.objects.filter(name__icontains=dest_name).first()
        if dest_obj:
            TouristAttraction.objects.update_or_create(
                destination=dest_obj,
                name=name,
                defaults={
                    'category': cat,
                    'description': desc,
                    'image_url': img,
                    'latitude': Decimal(str(lat)),
                    'longitude': Decimal(str(lng)),
                    'entry_fee': Decimal(str(fee)),
                    'typical_time_spent_hours': Decimal(str(hours)),
                    'is_indoor': indoor,
                    'rain_friendly': rain,
                    'rating': Decimal(str(rating))
                }
            )

    # --- 4. HOTELS FOR MAJOR DESTINATIONS ---
    hotels_data = [
        ('The Oberoi Amarvilas (Taj View)', 'Agra', 'Taj East Gate Road, Agra', 5, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80', 9500.00),
        ('The Himalayan Luxury Resort & Spa', 'Manali', 'Hadimba Temple Road, Manali', 4, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 4800.00),
        ('Le Grand Hotel Parisien', 'Paris', 'Boulevard Saint-Germain, Paris', 5, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80', 16500.00),
        ('Atlantis The Royal Resort & Beach', 'Dubai', 'Crescent Road, Palm Jumeirah, Dubai', 5, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 19000.00),
        ('Tokyo Shibuya Grand Central Hotel', 'Tokyo', 'Shibuya Dogenzaka, Tokyo', 4, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80', 11500.00),
        ('Ubud Hanging Gardens Wellness Resort', 'Bali', 'Buahan, Payangan, Gianyar, Bali', 5, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 7800.00),
    ]

    for hname, dest_name, addr, stars, img, base_p in hotels_data:
        dest_obj = dest_objs.get(dest_name) or Destination.objects.filter(name__icontains=dest_name).first()
        if dest_obj and provider:
            hotel, _ = Hotel.objects.update_or_create(
                name=hname,
                defaults={
                    'provider': provider,
                    'destination': dest_obj,
                    'address': addr,
                    'star_rating': stars,
                    'cover_image': img,
                    'base_price': Decimal(str(base_p)),
                    'cancellation_policy': 'Free cancellation up to 24 hours prior to check-in',
                    'amenities': 'WiFi, Air Conditioning, Panoramic Views, Swimming Pool, Complimentary Gourmet Breakfast'
                }
            )
            RoomType.objects.get_or_create(
                hotel=hotel,
                name='Deluxe Panoramic Room',
                defaults={
                    'description': 'Luxury room with king bed, marble bath, and scenic city/mountain views.',
                    'capacity_guests': 2,
                    'price_per_night': Decimal(str(base_p)),
                    'total_rooms': 10,
                    'available_rooms': 8
                }
            )

    print("[Success] All World Destinations, Activities, Attractions, and Accommodations populated!")

if __name__ == '__main__':
    seed_world_data()
