import json
import logging
from datetime import datetime
from sqlalchemy import text
from config.database import get_engine, fetch_all, fetch_one, execute_query

logger = logging.getLogger(__name__)


def init_schema_and_seed():
    """Initializes tables and seeds default data seamlessly for both SQLite and MySQL."""
    engine = get_engine()
    is_sqlite = "sqlite" in engine.url.drivername

    # Create tables if they do not exist
    with engine.begin() as conn:
        if is_sqlite:
            # SQLite compatible DDL
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                phone TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                travel_style TEXT DEFAULT 'Comfortable',
                preferred_budget_range TEXT DEFAULT '₹10,000 - ₹25,000',
                preferred_transport TEXT DEFAULT 'Train',
                preferred_accommodation TEXT DEFAULT 'Budget hotel',
                food_preference TEXT DEFAULT 'Local food',
                interests TEXT,
                accessibility_requirements TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                country TEXT DEFAULT 'India',
                state TEXT NOT NULL,
                city TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                description TEXT,
                best_season TEXT,
                ideal_duration_days INTEGER DEFAULT 3,
                avg_daily_budget REAL DEFAULT 3500.0,
                tags TEXT,
                image_url TEXT,
                is_popular BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS destination_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                category_name TEXT NOT NULL,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS attractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                entry_fee REAL DEFAULT 0.0,
                opening_time TEXT DEFAULT '09:00',
                closing_time TEXT DEFAULT '18:00',
                avg_visit_duration_hours REAL DEFAULT 2.0,
                latitude REAL,
                longitude REAL,
                is_indoor BOOLEAN DEFAULT 0,
                rating REAL DEFAULT 4.5,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price_per_person REAL NOT NULL,
                duration_hours REAL DEFAULT 2.0,
                suitable_for TEXT DEFAULT 'All',
                rating REAL DEFAULT 4.7,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                hotel_type TEXT DEFAULT 'Budget hotel',
                star_rating INTEGER DEFAULT 3,
                address TEXT,
                latitude REAL,
                longitude REAL,
                price_per_night REAL NOT NULL,
                amenities TEXT,
                rating REAL DEFAULT 4.2,
                image_url TEXT,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotel_id INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                capacity INTEGER DEFAULT 2,
                price_per_night REAL NOT NULL,
                available_count INTEGER DEFAULT 5,
                amenities TEXT,
                FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                cuisine_type TEXT NOT NULL,
                is_vegetarian BOOLEAN DEFAULT 0,
                avg_meal_cost REAL DEFAULT 300.0,
                address TEXT,
                rating REAL DEFAULT 4.3,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS transport_providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                code TEXT,
                contact_phone TEXT
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS transport_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider_id INTEGER,
                transport_type TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                carrier_name TEXT NOT NULL,
                service_number TEXT,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                duration_hours REAL NOT NULL,
                fare_economy REAL NOT NULL,
                fare_premium REAL DEFAULT 0.0,
                available_seats INTEGER DEFAULT 40,
                cancellation_policy TEXT,
                FOREIGN KEY (provider_id) REFERENCES transport_providers(id) ON DELETE SET NULL
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trip_name TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                days INTEGER NOT NULL,
                travelers_count INTEGER DEFAULT 1,
                traveler_type TEXT DEFAULT 'Solo',
                travel_style TEXT DEFAULT 'Comfortable',
                allocated_budget REAL NOT NULL,
                total_estimated_cost REAL NOT NULL,
                status TEXT DEFAULT 'Planned',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS itineraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS itinerary_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                itinerary_id INTEGER NOT NULL,
                day_number INTEGER NOT NULL,
                time_slot TEXT NOT NULL,
                activity_title TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                location_name TEXT,
                estimated_cost REAL DEFAULT 0.0,
                notes TEXT,
                FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                transport_cost REAL DEFAULT 0.0,
                accommodation_cost REAL DEFAULT 0.0,
                food_cost REAL DEFAULT 0.0,
                activities_cost REAL DEFAULT 0.0,
                local_transport_cost REAL DEFAULT 0.0,
                buffer_cost REAL DEFAULT 0.0,
                total_cost REAL DEFAULT 0.0,
                is_optimized BOOLEAN DEFAULT 0,
                savings_achieved REAL DEFAULT 0.0,
                FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trip_id INTEGER,
                booking_reference TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                provider_name TEXT NOT NULL,
                item_title TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                travel_date TEXT NOT NULL,
                passenger_count INTEGER DEFAULT 1,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'Confirmed',
                is_demo BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS booking_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                passenger_name TEXT NOT NULL,
                passenger_age INTEGER,
                seat_or_room TEXT,
                FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                payment_reference TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                payment_method TEXT DEFAULT 'DEMO_GATEWAY',
                payment_status TEXT DEFAULT 'SUCCESS',
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                destination_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                destination_id INTEGER NOT NULL,
                score REAL NOT NULL,
                reasons TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                weather_json TEXT NOT NULL,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS api_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT NOT NULL UNIQUE,
                response_json TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                role TEXT DEFAULT 'SUPER_ADMIN',
                permissions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))

    # Seed initial data if destinations is empty
    count = fetch_one("SELECT COUNT(*) as count FROM destinations")
    if not count or count["count"] == 0:
        seed_default_data()


def seed_default_data():
    """Seeds default destinations, users, hotels, attractions, transport, and restaurants."""
    logger.info("Seeding initial tourism platform data...")

    # Default Users (Password: Admin@123 / Traveler@123)
    # Using SHA256 hashed passwords
    from utils.authentication import hash_password
    default_pw = hash_password("Admin@123")
    user_pw = hash_password("Traveler@123")

    execute_query("""
    INSERT OR IGNORE INTO users (id, name, email, password_hash, phone, role) VALUES
    (1, 'System Administrator', 'admin@smarttourism.com', :pw1, '+91 9876543210', 'admin'),
    (2, 'Rohit Sharma', 'traveler@example.com', :pw2, '+91 9123456780', 'user')
    """, {"pw1": default_pw, "pw2": user_pw})

    execute_query("INSERT OR IGNORE INTO admin_users (user_id, role, permissions) VALUES (1, 'SUPER_ADMIN', 'ALL_ACCESS')")
    execute_query("""
    INSERT OR IGNORE INTO user_preferences (user_id, travel_style, preferred_budget_range, preferred_transport, preferred_accommodation, food_preference, interests)
    VALUES (2, 'Comfortable', '₹15,000 - ₹30,000', 'Train', 'Budget hotel', 'Local food', 'Nature, Photography, Adventure')
    """)

    # Destinations
    destinations = [
        (1, 'Araku Valley', 'India', 'Andhra Pradesh', 'Araku', 18.3273, 82.8775,
         'A serene hill station enveloped by Eastern Ghats, famous for lush coffee plantations, misty valleys, indigenous tribal culture, and ancient limestone caves.',
         'September to March', 3, 3000.00, 'Nature, Photography, Mountains, Culture, Coffee',
         'https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?w=800', 1),
        (2, 'Hyderabad', 'India', 'Telangana', 'Hyderabad', 17.3850, 78.4867,
         'The City of Pearls blending historic Charminar and Golconda Fort with modern HITEC City tech parks, renowned world over for Hyderabadi Dum Biryani.',
         'October to March', 3, 4000.00, 'History, Culture, Food, Architecture, Shopping',
         'https://images.unsplash.com/photo-1605342416110-60b72183c5fa?w=800', 1),
        (3, 'Warangal', 'India', 'Telangana', 'Warangal', 17.9689, 79.5941,
         'The historic capital of the Kakatiya dynasty known for the Thousand Pillar Temple, Warangal Fort, Ramappa Temple (UNESCO World Heritage), and Pakhal Lake.',
         'October to March', 2, 2500.00, 'History, Architecture, Religious, Photography',
         'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=800', 0),
        (4, 'Hampi', 'India', 'Karnataka', 'Hampi', 15.3350, 76.4600,
         'Magnificent UNESCO World Heritage site amidst boulder-strewn landscapes, boasting grand remnants of the 14th-century Vijayanagara Empire.',
         'October to February', 3, 2800.00, 'History, Architecture, Culture, Photography, Backpacker',
         'https://images.unsplash.com/photo-1600100397608-f010e588ac5e?w=800', 1),
        (5, 'Ooty', 'India', 'Tamil Nadu', 'Udhagamandalam', 11.4102, 76.6950,
         'Queen of Nilgiri Hill Stations boasting sprawling tea gardens, the Nilgiri Mountain Toy Train, Pykara waterfalls, and pleasant alpine climate.',
         'March to June, Sep to Nov', 3, 4500.00, 'Nature, Mountains, Romantic, Photography, Family',
         'https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?w=800', 1),
        (6, 'Jaipur', 'India', 'Rajasthan', 'Jaipur', 26.9124, 75.7873,
         'The Pink City filled with opulent royal palaces, Amber Fort, Hawa Mahal, bustling colorful bazaars, and vibrant Rajasthani heritage.',
         'October to March', 3, 4500.00, 'History, Culture, Architecture, Shopping, Photography',
         'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800', 1),
        (7, 'Varanasi', 'India', 'Uttar Pradesh', 'Varanasi', 25.3176, 82.9739,
         'One of the worlds oldest living cities on the sacred banks of River Ganga, renowned for spiritual evening Ganga Aarti, Ghats, and centuries-old silk weaving.',
         'November to March', 3, 2200.00, 'Religious, Spiritual, Culture, History, Photography',
         'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800', 1),
        (8, 'Goa', 'India', 'Goa', 'Panaji', 15.2993, 74.1240,
         'Tropical paradise featuring golden sand beaches, Portuguese colonial cathedrals, seaside shacks, spice plantations, and vibrant nightlife.',
         'November to February', 4, 5500.00, 'Beaches, Nightlife, Adventure, Food, Romantic',
         'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800', 1),
        (9, 'Munnar', 'India', 'Kerala', 'Munnar', 10.0889, 77.0595,
         'Rolling emerald hills blanketed by tea gardens, mist-clad peaks, Anamudi summit, cascading Cheeyappara falls, and cool mountain air.',
         'September to May', 3, 3800.00, 'Nature, Mountains, Romantic, Wildlife, Photography',
         'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=800', 1),
        (10, 'Gokarna', 'India', 'Karnataka', 'Gokarna', 14.5479, 74.3188,
         'A laid-back coastal pilgrimage town flanked by pristine cliff-side beaches including Om Beach, Kudle Beach, and Half Moon Beach.',
         'October to March', 3, 2200.00, 'Beaches, Adventure, Nature, Backpacker, Religious',
         'https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=800', 0)
    ]

    for d in destinations:
        execute_query("""
        INSERT OR IGNORE INTO destinations 
        (id, name, country, state, city, latitude, longitude, description, best_season, ideal_duration_days, avg_daily_budget, tags, image_url, is_popular)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, d)

    # Attractions
    attractions = [
        (1, 1, 'Borra Caves', 'Nature & Geology', 'Million-year-old limestone caves featuring majestic stalactite and stalagmite formations illuminated with colorful lights.', 80.0, '10:00', '17:00', 2.0, 18.2804, 83.0401, 1, 4.7),
        (2, 1, 'Katiki Waterfalls', 'Nature & Adventure', 'Spectacular 50-foot cascading waterfall situated amidst dense forest near Borra Caves, reached by local 4x4 jeep trek.', 20.0, '08:00', '16:30', 2.5, 18.2917, 83.0305, 0, 4.6),
        (3, 1, 'Araku Tribal Museum', 'Culture & History', 'Preserves indigenous tribal lifestyle, artifacts, handicrafts, clay dioramas, and archery equipment of Eastern Ghats tribes.', 40.0, '09:00', '18:00', 1.5, 18.3302, 82.8812, 1, 4.4),
        (4, 1, 'Chaparai Water Cascades', 'Nature & Leisure', 'Picturesque scenic picnic spot where stream waters glide over smooth sloping rock beds surrounded by lush forest.', 30.0, '09:00', '17:30', 2.0, 18.3050, 82.8550, 0, 4.5),
        (5, 1, 'Coffee Museum & Plantations', 'Food & Photography', 'Showcases the history of Araku Arabica coffee plantations with fresh organic coffee tastings, chocolates, and lush trails.', 50.0, '09:00', '19:00', 1.5, 18.3315, 82.8830, 0, 4.6),
        (6, 1, 'Padmapuram Botanical Gardens', 'Nature & Family', 'Historic garden established in 1942 featuring treetop hanging cottages, exotic flowers, and miniature toy train.', 40.0, '08:30', '18:00', 1.5, 18.3289, 82.8790, 0, 4.2),
        (7, 2, 'Golconda Fort', 'History & Architecture', 'Magnificent medieval fortress famed for acoustic architecture, royal palaces, and panoramic sunset views.', 25.0, '09:00', '17:30', 3.0, 17.3833, 78.4011, 0, 4.7),
        (8, 2, 'Charminar & Laad Bazaar', 'History & Shopping', '16th-century landmark mosque with 4 grand arches surrounded by historic pearl and bangle markets.', 20.0, '09:30', '19:00', 2.0, 17.3616, 78.4747, 0, 4.6),
        (9, 2, 'Salar Jung Museum', 'Museums & Art', 'One of the worlds largest one-man art collections housing the Veiled Rebecca and 19th-century musical clock.', 50.0, '10:00', '17:00', 3.0, 17.3713, 78.4804, 1, 4.8),
        (10, 3, 'Thousand Pillar Temple', 'History & Religious', '12th-century Kakatiya architectural marvel dedicated to Shiva, Vishnu, and Surya with finely carved stone pillars.', 0.0, '06:00', '20:00', 1.5, 17.9940, 79.5746, 0, 4.6),
        (11, 3, 'Warangal Fort & Stone Gateway', 'History & Architecture', 'Ancient ruins with massive ornamental Kakatiya thoranam arches adopted as the state emblem of Telangana.', 25.0, '09:00', '18:00', 2.0, 17.9575, 79.6178, 0, 4.5),
        (12, 3, 'Ramappa Temple', 'History & Architecture', 'UNESCO World Heritage monument celebrated for intricate sandbox foundations and lightweight floating bricks.', 30.0, '06:00', '18:00', 2.5, 18.2592, 79.9439, 0, 4.9)
    ]

    for a in attractions:
        execute_query("""
        INSERT OR IGNORE INTO attractions
        (id, destination_id, name, category, description, entry_fee, opening_time, closing_time, avg_visit_duration_hours, latitude, longitude, is_indoor, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, a)

    # Hotels
    hotels = [
        (1, 1, 'Haritha Valley Resort (APTDC)', 'Resort', 3, 'Near Padmapuram Gardens, Araku', 18.3280, 82.8795, 2200.0, 'Free Breakfast, Restaurant, Garden, Parking, Hot Water', 4.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'),
        (2, 1, 'Araku Tribal Homestay & Cottages', 'Homestay', 2, 'Main Road, Araku Valley', 18.3250, 82.8750, 1200.0, 'Local Cuisine, Campfire, Hot Water, Mountain View', 4.4, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800'),
        (3, 1, 'Nature Nest Valley View Hotel', 'Budget hotel', 2, 'Chaparai Road, Araku', 18.3210, 82.8720, 1500.0, 'WiFi, Room Service, Balcony, Doctor on call', 4.1, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'),
        (4, 1, 'Eastern Ghats Eco Luxury Glamping', 'Resort', 4, 'Coffee Estate Ridge, Araku', 18.3340, 82.8850, 4800.0, 'Luxury Tents, Organic Food, Guided Trek, Campfire, Spa', 4.8, 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800'),
        (5, 2, 'Taj Krishna Banjara Hills', '5-star', 5, 'Road No 1, Banjara Hills, Hyderabad', 17.4172, 78.4483, 8500.0, 'Pool, Spa, Fine Dining, Gym, Luxury Suites', 4.8, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800'),
        (6, 2, 'Hotel Deccan Heritage', 'Budget hotel', 3, 'Abids, Hyderabad', 17.3892, 78.4735, 1800.0, 'WiFi, AC, Breakfast, Parking', 4.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'),
        (7, 3, 'Hotel Ashoka Residency', 'Budget hotel', 2, 'Main Road, Hanamkonda, Warangal', 17.9890, 79.5850, 1400.0, 'WiFi, Restaurant, Hot Water, Room Service', 4.0, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'),
        (8, 3, 'Haritha Kakatiya Heritage Hotel', '3-star', 3, 'Subedari, Hanamkonda', 17.9870, 79.5820, 2400.0, 'Swimming Pool, Restaurant, Conference Hall, Bar', 4.3, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800'),
        (9, 1, 'Zostel Araku Valley Backpacker Hostel', 'Hostel', 3, 'Coffee Plantation Hills, Araku', 18.3300, 82.8810, 599.0, 'High-Speed Wi-Fi, Personal Lockers, Bunk Beds, Common Cafe, Board Games, Campfire', 4.7, 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800'),
        (10, 2, 'goSTOPS Hyderabad Youth & Backpacker Hostel', 'Hostel', 3, 'Gachibowli High Street, Hyderabad', 17.4401, 78.3489, 499.0, 'Air Conditioned Dorms, High-Speed Wi-Fi, Co-working Hub, Lockers, Laundry, 24/7 Reception', 4.6, 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'),
        (11, 2, 'The Hosteller Jubilee Hills', 'Hostel', 3, 'Road No 36, Jubilee Hills, Hyderabad', 17.4320, 78.4070, 699.0, 'Rooftop Lounge, Dedicated Workspaces, Female Dorms, Pod Beds, Community Kitchen', 4.8, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'),
        (12, 3, 'Warangal Heritage Backpacker Inn & Hostel', 'Hostel', 2, 'Near Fort Warangal Station, Warangal', 17.9620, 79.6100, 450.0, 'Free Wi-Fi, Secure Lockers, Hot Showers, Bike Rental, Common Terrace', 4.3, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800')
    ]

    for h in hotels:
        execute_query("""
        INSERT OR IGNORE INTO hotels
        (id, destination_id, name, hotel_type, star_rating, address, latitude, longitude, price_per_night, amenities, rating, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, h)

    # Transport Providers
    providers = [
        (1, 'Indian Railways (IRCTC)', 'Train', 'IRCTC', '139'),
        (2, 'IndiGo Airlines', 'Flight', '6E', '+91 9910383838'),
        (3, 'Air India Express', 'Flight', 'IX', '18602331407'),
        (4, 'APSRTC (Andhra Pradesh State Transport)', 'Bus', 'APSRTC', '0866-2570005'),
        (5, 'TSRTC (Telangana State Transport)', 'Bus', 'TSRTC', '040-69440000'),
        (6, 'Orange / Morning Star Travels', 'Bus', 'ORANGE', '040-33559999'),
        (7, 'Araku Valley Tourism Cabs & Rentals', 'Cab', 'ARAKU_CAB', '+91 9490012345')
    ]

    for p in providers:
        execute_query("INSERT OR IGNORE INTO transport_providers (id, name, type, code, contact_phone) VALUES (?, ?, ?, ?, ?)", p)

    # Transport Options
    routes = [
        (1, 1, 'Train', 'Hyderabad', 'Araku Valley', 'Visakha Express (17016 / 58501 Vistadome)', '17016', '16:50', '08:45', 15.9, 450.0, 1250.0, 48, 'Full refund minus ₹60 before 48 hrs'),
        (2, 1, 'Train', 'Hyderabad', 'Araku Valley', 'Godavari Superfast Express + Passenger', '12728', '17:05', '09:15', 16.1, 480.0, 1350.0, 32, 'Standard IRCTC rules apply'),
        (3, 4, 'Bus', 'Hyderabad', 'Araku Valley', 'APSRTC Amaravathi AC Multi-Axle', 'AP-9021', '19:30', '09:00', 13.5, 950.0, 1400.0, 24, 'Free cancellation up to 12 hours before'),
        (4, 6, 'Bus', 'Hyderabad', 'Araku Valley', 'Orange Volvo AC Sleeper', 'OR-4421', '20:15', '09:30', 13.25, 1200.0, 1750.0, 18, 'Non-refundable within 4 hours'),
        (5, 7, 'Cab', 'Hyderabad', 'Araku Valley', 'Dedicated Sedan Taxi (Outstation 3 Days)', 'CAB-SEDAN', 'Flexible', 'Flexible', 12.0, 7500.0, 9500.0, 4, 'Free cancellation up to 24 hrs before departure'),
        (6, 2, 'Flight', 'Hyderabad', 'Araku Valley', 'IndiGo (HYD to VSKP) + Connecting Cab', '6E-452', '06:15', '09:45', 3.5, 3400.0, 5800.0, 15, 'Cancellation fee ₹2500 applies'),
        (7, 1, 'Train', 'Hyderabad', 'Warangal', 'Satavahana Express', '12714', '16:25', '18:50', 2.4, 90.0, 320.0, 75, 'Standard IRCTC rules'),
        (8, 5, 'Bus', 'Hyderabad', 'Warangal', 'TSRTC Super Luxury Express', 'TS-102', 'Every 30m', 'Every 30m', 2.8, 180.0, 250.0, 36, 'Full refund up to 2 hrs before'),
        (9, 7, 'Cab', 'Hyderabad', 'Warangal', 'One-way Sedan Cab', 'CAB-WGL', 'Flexible', 'Flexible', 2.5, 2200.0, 2800.0, 4, 'Free cancellation up to 4 hrs before')
    ]

    for r in routes:
        execute_query("""
        INSERT OR IGNORE INTO transport_options
        (id, provider_id, transport_type, origin, destination, carrier_name, service_number, departure_time, arrival_time, duration_hours, fare_economy, fare_premium, available_seats, cancellation_policy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, r)

    # Activities
    activities = [
        (1, 1, 'Guided Borra Caves Exploration', 'Adventure & Heritage', 'Expert speleologist guide explaining million-year-old rock formations and hidden caverns.', 250.0, 2.0, 'All', 4.8),
        (2, 1, 'Dhimsa Tribal Folk Dance Experience', 'Culture', 'Authentic evening performance of traditional Dhimsa tribal community dance with live folk instruments.', 200.0, 1.5, 'Family, Couple, Culture lovers', 4.7),
        (3, 1, 'Coffee Plantation Walk & Bean-to-Cup Tasting', 'Culinary & Nature', 'Stroll through organic Arabica coffee slopes, learn harvesting techniques, and savor freshly ground brew.', 350.0, 2.5, 'All', 4.9),
        (4, 1, 'Katiki Waterfalls 4x4 Off-Road Trek', 'Adventure', 'Thrilling jeep safari navigating bumpy rocky forest streams up to the cascading waterfalls.', 400.0, 3.0, 'Adventure, Friends, Couples', 4.8),
        (5, 2, 'Heritage Walk of Charminar & Old City', 'Culture & History', 'Narrated walking tour across historic streets, century-old bakeries, and perfumeries.', 300.0, 2.5, 'All', 4.8),
        (6, 2, 'Hussain Sagar Sunset Yacht Cruise', 'Romantic & Leisure', 'Private leisurely boat ride along the lake admiring the illuminated Buddha statue.', 800.0, 1.5, 'Couple, Family', 4.6)
    ]

    for act in activities:
        execute_query("""
        INSERT OR IGNORE INTO activities
        (id, destination_id, title, category, description, price_per_person, duration_hours, suitable_for, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, act)

    # Restaurants
    restaurants = [
        (1, 1, 'Vasundhara Andhra Restaurant', 'Local Andhra & Vegetarian', 1, 180.0, 'Main Road, Araku', 4.4),
        (2, 1, 'Araku Valley Bamboo Chicken & Tribal Kitchen', 'Authentic Tribal Non-Veg & Veg', 0, 250.0, 'Near Borra Caves junction', 4.6),
        (3, 1, 'Sri Annapurna Pure Veg Tiffins', 'South Indian Pure Veg', 1, 120.0, 'Opposite Railway Station, Araku', 4.3),
        (4, 2, 'Paradise Food Court', 'Hyderabadi Biryani & Mughlai', 0, 350.0, 'Secunderabad & Banjara Hills, Hyderabad', 4.5),
        (5, 2, 'Chutneys', 'South Indian Vegetarian & Babai Hotel Ghee Idli', 1, 220.0, 'Road No 3, Banjara Hills, Hyderabad', 4.7)
    ]

    for res in restaurants:
        execute_query("""
        INSERT OR IGNORE INTO restaurants
        (id, destination_id, name, cuisine_type, is_vegetarian, avg_meal_cost, address, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, res)

    logger.info("Database successfully seeded.")


# ----------------------------------------------------------------------
# USER & AUTH QUERIES
# ----------------------------------------------------------------------

def get_user_by_email(email):
    return fetch_one("SELECT * FROM users WHERE email = :email", {"email": email.strip().lower()})


def get_user_by_id(user_id):
    return fetch_one("SELECT * FROM users WHERE id = :id", {"id": user_id})


def create_user(name, email, password_hash, phone=""):
    user_id = execute_query(
        "INSERT INTO users (name, email, password_hash, phone, role) VALUES (:name, :email, :pw, :phone, 'user')",
        {"name": name.strip(), "email": email.strip().lower(), "pw": password_hash, "phone": phone.strip()}
    )
    # Default preferences
    execute_query(
        "INSERT INTO user_preferences (user_id, travel_style, preferred_budget_range, preferred_transport, preferred_accommodation, food_preference, interests) "
        "VALUES (:uid, 'Comfortable', '₹10,000 - ₹25,000', 'Train', 'Budget hotel', 'Local food', 'Nature, Culture')",
        {"uid": user_id}
    )
    return user_id


def get_user_preferences(user_id):
    return fetch_one("SELECT * FROM user_preferences WHERE user_id = :uid", {"uid": user_id})


def update_user_preferences(user_id, style, budget, transport, accommodation, food, interests, accessibility=""):
    execute_query("""
    INSERT INTO user_preferences (user_id, travel_style, preferred_budget_range, preferred_transport, preferred_accommodation, food_preference, interests, accessibility_requirements)
    VALUES (:uid, :style, :budget, :transport, :accommodation, :food, :interests, :access)
    ON CONFLICT(user_id) DO UPDATE SET
        travel_style=excluded.travel_style,
        preferred_budget_range=excluded.preferred_budget_range,
        preferred_transport=excluded.preferred_transport,
        preferred_accommodation=excluded.preferred_accommodation,
        food_preference=excluded.food_preference,
        interests=excluded.interests,
        accessibility_requirements=excluded.accessibility_requirements,
        updated_at=CURRENT_TIMESTAMP
    """, {
        "uid": user_id, "style": style, "budget": budget, "transport": transport,
        "accommodation": accommodation, "food": food, "interests": interests, "access": accessibility
    })


# ----------------------------------------------------------------------
# DESTINATION QUERIES
# ----------------------------------------------------------------------

def get_all_destinations(limit=100):
    return fetch_all("SELECT * FROM destinations ORDER BY is_popular DESC, name ASC LIMIT :limit", {"limit": limit})


def get_destination_by_name(name):
    return fetch_one(
        "SELECT * FROM destinations WHERE LOWER(name) = :name OR LOWER(city) = :name LIMIT 1",
        {"name": name.strip().lower()}
    )


def search_destinations(keyword):
    pattern = f"%{keyword.strip().lower()}%"
    return fetch_all("""
        SELECT * FROM destinations 
        WHERE LOWER(name) LIKE :pattern 
           OR LOWER(city) LIKE :pattern 
           OR LOWER(state) LIKE :pattern 
           OR LOWER(tags) LIKE :pattern
        ORDER BY is_popular DESC, name ASC
    """, {"pattern": pattern})


def save_destination(name, state, city, lat, lon, description, tags, image_url="", best_season="All year", avg_daily_budget=3000.0, ideal_duration_days=3):
    return execute_query("""
        INSERT INTO destinations (name, country, state, city, latitude, longitude, description, best_season, ideal_duration_days, avg_daily_budget, tags, image_url, is_popular)
        VALUES (:name, 'India', :state, :city, :lat, :lon, :desc, :season, :duration, :budget, :tags, :img, 0)
    """, {
        "name": name, "state": state, "city": city, "lat": lat, "lon": lon,
        "desc": description, "season": best_season, "duration": ideal_duration_days,
        "budget": avg_daily_budget, "tags": tags, "img": image_url
    })


def get_attractions_by_destination(destination_id):
    return fetch_all("SELECT * FROM attractions WHERE destination_id = :did ORDER BY rating DESC", {"did": destination_id})


def get_hotels_by_destination(destination_id):
    return fetch_all("SELECT * FROM hotels WHERE destination_id = :did ORDER BY rating DESC", {"did": destination_id})


def get_activities_by_destination(destination_id):
    return fetch_all("SELECT * FROM activities WHERE destination_id = :did ORDER BY rating DESC", {"did": destination_id})


def get_restaurants_by_destination(destination_id):
    return fetch_all("SELECT * FROM restaurants WHERE destination_id = :did ORDER BY rating DESC", {"did": destination_id})


# ----------------------------------------------------------------------
# TRANSPORT QUERIES
# ----------------------------------------------------------------------

def get_transport_options(origin, destination, transport_type=None):
    query = """
    SELECT * FROM transport_options 
    WHERE (LOWER(origin) LIKE :origin OR :origin LIKE '%' || LOWER(origin) || '%')
      AND (LOWER(destination) LIKE :dest OR :dest LIKE '%' || LOWER(destination) || '%')
    """
    params = {"origin": f"%{origin.strip().lower()}%", "dest": f"%{destination.strip().lower()}%"}
    if transport_type and transport_type != "All":
        query += " AND LOWER(transport_type) = :type"
        params["type"] = transport_type.lower()
    query += " ORDER BY fare_economy ASC"
    return fetch_all(query, params)


# ----------------------------------------------------------------------
# TRIP & ITINERARY QUERIES
# ----------------------------------------------------------------------

def save_trip(user_id, trip_name, origin, destination, start_date, end_date, days, travelers_count, traveler_type, travel_style, allocated_budget, total_estimated_cost):
    return execute_query("""
    INSERT INTO trips (user_id, trip_name, origin, destination, start_date, end_date, days, travelers_count, traveler_type, travel_style, allocated_budget, total_estimated_cost, status)
    VALUES (:uid, :name, :origin, :dest, :start, :end, :days, :tcount, :ttype, :tstyle, :budget, :cost, 'Planned')
    """, {
        "uid": user_id, "name": trip_name, "origin": origin, "dest": destination,
        "start": str(start_date), "end": str(end_date), "days": days,
        "tcount": travelers_count, "ttype": traveler_type, "tstyle": travel_style,
        "budget": allocated_budget, "cost": total_estimated_cost
    })


def get_user_trips(user_id):
    return fetch_all("SELECT * FROM trips WHERE user_id = :uid ORDER BY id DESC", {"uid": user_id})


def get_trip_by_id(trip_id):
    return fetch_one("SELECT * FROM trips WHERE id = :tid", {"tid": trip_id})


def save_itinerary(trip_id, items):
    itinerary_id = execute_query("INSERT INTO itineraries (trip_id) VALUES (:tid)", {"tid": trip_id})
    for item in items:
        execute_query("""
        INSERT INTO itinerary_items (itinerary_id, day_number, time_slot, activity_title, activity_type, location_name, estimated_cost, notes)
        VALUES (:itid, :day, :slot, :title, :type, :loc, :cost, :notes)
        """, {
            "itid": itinerary_id, "day": item.get("day", 1), "slot": item.get("time_slot", ""),
            "title": item.get("activity_title", ""), "type": item.get("activity_type", "Sightseeing"),
            "loc": item.get("location_name", ""), "cost": item.get("estimated_cost", 0.0),
            "notes": item.get("notes", "")
        })
    return itinerary_id


def get_trip_itinerary(trip_id):
    itinerary = fetch_one("SELECT * FROM itineraries WHERE trip_id = :tid ORDER BY id DESC LIMIT 1", {"tid": trip_id})
    if not itinerary:
        return []
    return fetch_all("SELECT * FROM itinerary_items WHERE itinerary_id = :itid ORDER BY day_number ASC, id ASC", {"itid": itinerary["id"]})


def save_budget(trip_id, transport_cost, accommodation_cost, food_cost, activities_cost, local_transport_cost, buffer_cost, total_cost, is_optimized=False, savings=0.0):
    return execute_query("""
    INSERT INTO budgets (trip_id, transport_cost, accommodation_cost, food_cost, activities_cost, local_transport_cost, buffer_cost, total_cost, is_optimized, savings_achieved)
    VALUES (:tid, :tc, :ac, :fc, :act, :ltc, :buf, :tot, :opt, :sav)
    """, {
        "tid": trip_id, "tc": transport_cost, "ac": accommodation_cost, "fc": food_cost,
        "act": activities_cost, "ltc": local_transport_cost, "buf": buffer_cost,
        "tot": total_cost, "opt": 1 if is_optimized else 0, "sav": savings
    })


def get_trip_budget(trip_id):
    return fetch_one("SELECT * FROM budgets WHERE trip_id = :tid ORDER BY id DESC LIMIT 1", {"tid": trip_id})


# ----------------------------------------------------------------------
# BOOKING & PAYMENT QUERIES
# ----------------------------------------------------------------------

def create_booking(user_id, trip_id, booking_ref, category, provider, item_title, travel_date, passenger_count, total_amount, is_demo=True):
    booking_id = execute_query("""
    INSERT INTO bookings (user_id, trip_id, booking_reference, category, provider_name, item_title, booking_date, travel_date, passenger_count, total_amount, status, is_demo)
    VALUES (:uid, :tid, :ref, :cat, :provider, :title, :bdate, :tdate, :pcount, :amt, 'Confirmed', :demo)
    """, {
        "uid": user_id, "tid": trip_id, "ref": booking_ref, "cat": category,
        "provider": provider, "title": item_title, "bdate": datetime.now().strftime("%Y-%m-%d"),
        "tdate": str(travel_date), "pcount": passenger_count, "amt": total_amount, "demo": 1 if is_demo else 0
    })
    return booking_id


def record_payment(booking_id, payment_ref, amount, method="DEMO_PAYMENT", status="SUCCESS"):
    return execute_query("""
    INSERT INTO payments (booking_id, payment_reference, amount, currency, payment_method, payment_status)
    VALUES (:bid, :pref, :amt, 'INR', :method, :status)
    """, {
        "bid": booking_id, "pref": payment_ref, "amt": amount, "method": method, "status": status
    })


def get_user_bookings(user_id, category=None):
    query = "SELECT * FROM bookings WHERE user_id = :uid"
    params = {"uid": user_id}
    if category and category != "All":
        query += " AND category = :cat"
        params["cat"] = category
    query += " ORDER BY id DESC"
    return fetch_all(query, params)


def cancel_booking(booking_id, user_id):
    execute_query("UPDATE bookings SET status = 'Cancelled' WHERE id = :bid AND user_id = :uid", {"bid": booking_id, "uid": user_id})


# ----------------------------------------------------------------------
# AUDIT & ADMIN QUERIES
# ----------------------------------------------------------------------

def log_audit(user_id, action, details="", ip="127.0.0.1"):
    execute_query("INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (:uid, :act, :det, :ip)",
                  {"uid": user_id, "act": action, "det": details, "ip": ip})


def get_admin_metrics():
    total_users = fetch_one("SELECT COUNT(*) as cnt FROM users")["cnt"]
    total_bookings = fetch_one("SELECT COUNT(*) as cnt FROM bookings")["cnt"]
    total_revenue = fetch_one("SELECT COALESCE(SUM(total_amount), 0) as rev FROM bookings WHERE status = 'Confirmed'")["rev"]
    total_destinations = fetch_one("SELECT COUNT(*) as cnt FROM destinations")["cnt"]
    recent_bookings = fetch_all("SELECT * FROM bookings ORDER BY id DESC LIMIT 10")
    audit_logs = fetch_all("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 15")
    return {
        "users": total_users,
        "bookings": total_bookings,
        "revenue": total_revenue,
        "destinations": total_destinations,
        "recent_bookings": recent_bookings,
        "audit_logs": audit_logs
    }
