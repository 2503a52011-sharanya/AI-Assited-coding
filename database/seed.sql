-- =============================================================================
-- SMART TOURISM SYSTEM INITIAL SEED DATA
-- Includes Indian Destinations (Major, Small Towns, Nature, Heritage),
-- Hotels, Attractions, Transport Routes, Activities, and Default Accounts.
-- =============================================================================

USE smart_tourism;

-- 1. SEED DEFAULT USERS (Passwords hashed: Admin@123 -> $2b$12$e8x... or pbkdf2)
-- Using SHA256 hashed / passlib compatible hashes
INSERT INTO users (id, name, email, password_hash, phone, role) VALUES
(1, 'System Administrator', 'admin@smarttourism.com', '$2b$12$zI0E7kYtPkyQzPzZ3p7Hve72uYn5UaQjW6rK1c/g1n6rV2kHh7O3W', '+91 9876543210', 'admin'),
(2, 'Rohit Sharma', 'traveler@example.com', '$2b$12$zI0E7kYtPkyQzPzZ3p7Hve72uYn5UaQjW6rK1c/g1n6rV2kHh7O3W', '+91 9123456780', 'user')
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO admin_users (user_id, role, permissions) VALUES
(1, 'SUPER_ADMIN', 'ALL_ACCESS')
ON DUPLICATE KEY UPDATE role=VALUES(role);

INSERT INTO user_preferences (user_id, travel_style, preferred_budget_range, preferred_transport, preferred_accommodation, food_preference, interests) VALUES
(2, 'Comfortable', '₹15,000 - ₹30,000', 'Train', 'Budget hotel', 'Local food', 'Nature, Photography, Adventure')
ON DUPLICATE KEY UPDATE travel_style=VALUES(travel_style);

-- 2. SEED DESTINATIONS (Small town, hill station, heritage, coastal, major city)
INSERT INTO destinations (id, name, country, state, city, latitude, longitude, description, best_season, ideal_duration_days, avg_daily_budget, tags, image_url, is_popular) VALUES
(1, 'Araku Valley', 'India', 'Andhra Pradesh', 'Araku', 18.3273, 82.8775, 
 'A serene hill station enveloped by Eastern Ghats, famous for lush coffee plantations, misty valleys, indigenous tribal culture, and ancient limestone caves.', 
 'September to March', 3, 3000.00, 'Nature, Photography, Mountains, Culture, Coffee', 'https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?w=800', TRUE),

(2, 'Hyderabad', 'India', 'Telangana', 'Hyderabad', 17.3850, 78.4867, 
 'The City of Pearls blending historic Charminar and Golconda Fort with modern HITEC City tech parks, renowned world over for Hyderabadi Dum Biryani.', 
 'October to March', 3, 4000.00, 'History, Culture, Food, Architecture, Shopping', 'https://images.unsplash.com/photo-1605342416110-60b72183c5fa?w=800', TRUE),

(3, 'Warangal', 'India', 'Telangana', 'Warangal', 17.9689, 79.5941, 
 'The historic capital of the Kakatiya dynasty known for the Thousand Pillar Temple, Warangal Fort, Ramappa Temple (UNESCO World Heritage), and Pakhal Lake.', 
 'October to March', 2, 2500.00, 'History, Architecture, Religious, Photography', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=800', FALSE),

(4, 'Hampi', 'India', 'Karnataka', 'Hampi', 15.3350, 76.4600, 
 'Magnificent UNESCO World Heritage site amidst boulder-strewn landscapes, boasting grand remnants of the 14th-century Vijayanagara Empire.', 
 'October to February', 3, 2800.00, 'History, Architecture, Culture, Photography, Backpacker', 'https://images.unsplash.com/photo-1600100397608-f010e588ac5e?w=800', TRUE),

(5, 'Ooty', 'India', 'Tamil Nadu', 'Udhagamandalam', 11.4102, 76.6950, 
 'Queen of Nilgiri Hill Stations boasting sprawling tea gardens, the Nilgiri Mountain Toy Train, Pykara waterfalls, and pleasant alpine climate.', 
 'March to June, Sep to Nov', 3, 4500.00, 'Nature, Mountains, Romantic, Photography, Family', 'https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?w=800', TRUE),

(6, 'Jaipur', 'India', 'Rajasthan', 'Jaipur', 26.9124, 75.7873, 
 'The Pink City filled with opulent royal palaces, Amber Fort, Hawa Mahal, bustling colorful bazaars, and vibrant Rajasthani heritage.', 
 'October to March', 3, 4500.00, 'History, Culture, Architecture, Shopping, Photography', 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800', TRUE),

(7, 'Varanasi', 'India', 'Uttar Pradesh', 'Varanasi', 25.3176, 82.9739, 
 'One of the world’s oldest living cities on the sacred banks of River Ganga, renowned for spiritual evening Ganga Aarti, Ghats, and centuries-old silk weaving.', 
 'November to March', 3, 2200.00, 'Religious, Spiritual, Culture, History, Photography', 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800', TRUE),

(8, 'Goa', 'India', 'Goa', 'Panaji', 15.2993, 74.1240, 
 'Tropical paradise featuring golden sand beaches, Portuguese colonial cathedrals, seaside shacks, spice plantations, and vibrant nightlife.', 
 'November to February', 4, 5500.00, 'Beaches, Nightlife, Adventure, Food, Romantic', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800', TRUE),

(9, 'Munnar', 'India', 'Kerala', 'Munnar', 10.0889, 77.0595, 
 'Rolling emerald hills blanketed by tea gardens, mist-clad peaks, Anamudi summit, cascading Cheeyappara falls, and cool mountain air.', 
 'September to May', 3, 3800.00, 'Nature, Mountains, Romantic, Wildlife, Photography', 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=800', TRUE),

(10, 'Gokarna', 'India', 'Karnataka', 'Gokarna', 14.5479, 74.3188, 
 'A laid-back coastal pilgrimage town flanked by pristine cliff-side beaches including Om Beach, Kudle Beach, and Half Moon Beach.', 
 'October to March', 3, 2200.00, 'Beaches, Adventure, Nature, Backpacker, Religious', 'https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=800', FALSE)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 3. SEED ATTRACTIONS FOR ARAKU VALLEY & OTHERS
INSERT INTO attractions (id, destination_id, name, category, description, entry_fee, opening_time, closing_time, avg_visit_duration_hours, latitude, longitude, is_indoor, rating) VALUES
(1, 1, 'Borra Caves', 'Nature & Geology', 'Million-year-old limestone caves featuring majestic stalactite and stalagmite formations illuminated with colorful lights.', 80.00, '10:00', '17:00', 2.0, 18.2804, 83.0401, TRUE, 4.7),
(2, 1, 'Katiki Waterfalls', 'Nature & Adventure', 'Spectacular 50-foot cascading waterfall situated amidst dense forest near Borra Caves, reached by local 4x4 jeep trek.', 20.00, '08:00', '16:30', 2.5, 18.2917, 83.0305, FALSE, 4.6),
(3, 1, 'Araku Tribal Museum', 'Culture & History', 'Preserves indigenous tribal lifestyle, artifacts, handicrafts, clay dioramas, and archery equipment of Eastern Ghats tribes.', 40.00, '09:00', '18:00', 1.5, 18.3302, 82.8812, TRUE, 4.4),
(4, 1, 'Chaparai Water Cascades', 'Nature & Leisure', 'Picturesque scenic picnic spot where stream waters glide over smooth sloping rock beds surrounded by lush forest.', 30.00, '09:00', '17:30', 2.0, 18.3050, 82.8550, FALSE, 4.5),
(5, 1, 'Coffee Museum & Plantations', 'Food & Photography', 'Showcases the history of Araku Arabica coffee plantations with fresh organic coffee tastings, chocolates, and lush trails.', 50.00, '09:00', '19:00', 1.5, 18.3315, 82.8830, FALSE, 4.6),
(6, 1, 'Padmapuram Botanical Gardens', 'Nature & Family', 'Historic garden established in 1942 featuring treetop hanging cottages, exotic flowers, and miniature toy train.', 40.00, '08:30', '18:00', 1.5, 18.3289, 82.8790, FALSE, 4.2),

-- Hyderabad Attractions
(7, 2, 'Golconda Fort', 'History & Architecture', 'Magnificent medieval fortress famed for acoustic architecture, royal palaces, and panoramic sunset views.', 25.00, '09:00', '17:30', 3.0, 17.3833, 78.4011, FALSE, 4.7),
(8, 2, 'Charminar & Laad Bazaar', 'History & Shopping', '16th-century landmark mosque with 4 grand arches surrounded by historic pearl and bangle markets.', 20.00, '09:30', '19:00', 2.0, 17.3616, 78.4747, FALSE, 4.6),
(9, 2, 'Salar Jung Museum', 'Museums & Art', 'One of the world’s largest one-man art collections housing the Veiled Rebecca and 19th-century musical clock.', 50.00, '10:00', '17:00', 3.0, 17.3713, 78.4804, TRUE, 4.8),

-- Warangal Attractions
(10, 3, 'Thousand Pillar Temple', 'History & Religious', '12th-century Kakatiya architectural marvel dedicated to Shiva, Vishnu, and Surya with finely carved stone pillars.', 0.00, '06:00', '20:00', 1.5, 17.9940, 79.5746, FALSE, 4.6),
(11, 3, 'Warangal Fort & Stone Gateway', 'History & Architecture', 'Ancient ruins with massive ornamental Kakatiya thoranam arches adopted as the state emblem of Telangana.', 25.00, '09:00', '18:00', 2.0, 17.9575, 79.6178, FALSE, 4.5),
(12, 3, 'Ramappa Temple', 'History & Architecture', 'UNESCO World Heritage monument celebrated for intricate sandbox foundations and lightweight floating bricks.', 30.00, '06:00', '18:00', 2.5, 18.2592, 79.9439, FALSE, 4.9)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 4. SEED HOTELS (Budget, Mid-range, Resort, Homestay)
INSERT INTO hotels (id, destination_id, name, hotel_type, star_rating, address, latitude, longitude, price_per_night, amenities, rating, image_url) VALUES
(1, 1, 'Haritha Valley Resort (APTDC)', 'Resort', 3, 'Near Padmapuram Gardens, Araku', 18.3280, 82.8795, 2200.00, 'Free Breakfast, Restaurant, Garden, Parking, Hot Water', 4.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'),
(2, 1, 'Araku Tribal Homestay & Cottages', 'Homestay', 2, 'Main Road, Araku Valley', 18.3250, 82.8750, 1200.00, 'Local Cuisine, Campfire, Hot Water, Mountain View', 4.4, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800'),
(3, 1, 'Nature Nest Valley View Hotel', 'Budget hotel', 2, 'Chaparai Road, Araku', 18.3210, 82.8720, 1500.00, 'WiFi, Room Service, Balcony, Doctor on call', 4.1, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'),
(4, 1, 'Eastern Ghats Eco Luxury Glamping', 'Resort', 4, 'Coffee Estate Ridge, Araku', 18.3340, 82.8850, 4800.00, 'Luxury Tents, Organic Food, Guided Trek, Campfire, Spa', 4.8, 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800'),

-- Hyderabad Hotels
(5, 2, 'Taj Krishna Banjara Hills', '5-star', 5, 'Road No 1, Banjara Hills, Hyderabad', 17.4172, 78.4483, 8500.00, 'Pool, Spa, Fine Dining, Gym, Luxury Suites', 4.8, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800'),
(6, 2, 'Hotel Deccan Heritage', 'Budget hotel', 3, 'Abids, Hyderabad', 17.3892, 78.4735, 1800.00, 'WiFi, AC, Breakfast, Parking', 4.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'),

-- Warangal Hotels
(7, 3, 'Hotel Ashoka Residency', 'Budget hotel', 2, 'Main Road, Hanamkonda, Warangal', 17.9890, 79.5850, 1400.00, 'WiFi, Restaurant, Hot Water, Room Service', 4.0, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800'),
(8, 3, 'Haritha Kakatiya Heritage Hotel', '3-star', 3, 'Subedari, Hanamkonda', 17.9870, 79.5820, 2400.00, 'Swimming Pool, Restaurant, Conference Hall, Bar', 4.3, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 5. SEED TRANSPORT PROVIDERS
INSERT INTO transport_providers (id, name, type, code, contact_phone) VALUES
(1, 'Indian Railways (IRCTC)', 'Train', 'IRCTC', '139'),
(2, 'IndiGo Airlines', 'Flight', '6E', '+91 9910383838'),
(3, 'Air India Express', 'Flight', 'IX', '18602331407'),
(4, 'APSRTC (Andhra Pradesh State Transport)', 'Bus', 'APSRTC', '0866-2570005'),
(5, 'TSRTC (Telangana State Transport)', 'Bus', 'TSRTC', '040-69440000'),
(6, 'Orange / Morning Star Travels', 'Bus', 'ORANGE', '040-33559999'),
(7, 'Araku Valley Tourism Cabs & Rentals', 'Cab', 'ARAKU_CAB', '+91 9490012345')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 6. SEED TRANSPORT ROUTES (e.g. Hyderabad -> Araku Valley via Visakhapatnam / Direct)
INSERT INTO transport_options (id, provider_id, transport_type, origin, destination, carrier_name, service_number, departure_time, arrival_time, duration_hours, fare_economy, fare_premium, available_seats, cancellation_policy) VALUES
-- Hyderabad to Araku Valley (Train via VSKP or Direct Express)
(1, 1, 'Train', 'Hyderabad', 'Araku Valley', 'Visakha Express (17016 / 58501 Vistadome)', '17016', '16:50', '08:45', 15.9, 450.00, 1250.00, 48, 'Full refund minus ₹60 before 48 hrs'),
(2, 1, 'Train', 'Hyderabad', 'Araku Valley', 'Godavari Superfast Express + Passenger', '12728', '17:05', '09:15', 16.1, 480.00, 1350.00, 32, 'Standard IRCTC rules apply'),
(3, 4, 'Bus', 'Hyderabad', 'Araku Valley', 'APSRTC Amaravathi AC Multi-Axle', 'AP-9021', '19:30', '09:00', 13.5, 950.00, 1400.00, 24, 'Free cancellation up to 12 hours before'),
(4, 6, 'Bus', 'Hyderabad', 'Araku Valley', 'Orange Volvo AC Sleeper', 'OR-4421', '20:15', '09:30', 13.25, 1200.00, 1750.00, 18, 'Non-refundable within 4 hours'),
(5, 7, 'Cab', 'Hyderabad', 'Araku Valley', 'Dedicated Sedan Taxi (Outstation 3 Days)', 'CAB-SEDAN', 'Flexible', 'Flexible', 12.0, 7500.00, 9500.00, 4, 'Free cancellation up to 24 hrs before departure'),
(6, 2, 'Flight', 'Hyderabad', 'Araku Valley', 'IndiGo (HYD to VSKP) + Connecting Cab', '6E-452', '06:15', '09:45', 3.5, 3400.00, 5800.00, 15, 'Cancellation fee ₹2500 applies'),

-- Hyderabad to Warangal
(7, 1, 'Train', 'Hyderabad', 'Warangal', 'Satavahana Express', '12714', '16:25', '18:50', 2.4, 90.00, 320.00, 75, 'Standard IRCTC rules'),
(8, 5, 'Bus', 'Hyderabad', 'Warangal', 'TSRTC Super Luxury Express', 'TS-102', 'Every 30m', 'Every 30m', 2.8, 180.00, 250.00, 36, 'Full refund up to 2 hrs before'),
(9, 7, 'Cab', 'Hyderabad', 'Warangal', 'One-way Sedan Cab', 'CAB-WGL', 'Flexible', 'Flexible', 2.5, 2200.00, 2800.00, 4, 'Free cancellation up to 4 hrs before')
ON DUPLICATE KEY UPDATE carrier_name=VALUES(carrier_name);

-- 7. SEED ACTIVITIES FOR ARAKU
INSERT INTO activities (id, destination_id, title, category, description, price_per_person, duration_hours, suitable_for, rating) VALUES
(1, 1, 'Guided Borra Caves Exploration', 'Adventure & Heritage', 'Expert speleologist guide explaining million-year-old rock formations and hidden caverns.', 250.00, 2.0, 'All', 4.8),
(2, 1, 'Dhimsa Tribal Folk Dance Experience', 'Culture', 'Authentic evening performance of traditional Dhimsa tribal community dance with live folk instruments.', 200.00, 1.5, 'Family, Couple, Culture lovers', 4.7),
(3, 1, 'Coffee Plantation Walk & Bean-to-Cup Tasting', 'Culinary & Nature', 'Stroll through organic Arabica coffee slopes, learn harvesting techniques, and savor freshly ground brew.', 350.00, 2.5, 'All', 4.9),
(4, 1, 'Katiki Waterfalls 4x4 Off-Road Trek', 'Adventure', 'Thrilling jeep safari navigating bumpy rocky forest streams up to the cascading waterfalls.', 400.00, 3.0, 'Adventure, Friends, Couples', 4.8),

-- Hyderabad Activities
(5, 2, 'Heritage Walk of Charminar & Old City', 'Culture & History', 'Narrated walking tour across historic streets, century-old bakeries, and perfumeries.', 300.00, 2.5, 'All', 4.8),
(6, 2, 'Hussain Sagar Sunset Yacht Cruise', 'Romantic & Leisure', 'Private leisurely boat ride along the lake admiring the illuminated Buddha statue.', 800.00, 1.5, 'Couple, Family', 4.6)
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- 8. SEED RESTAURANTS
INSERT INTO restaurants (id, destination_id, name, cuisine_type, is_vegetarian, avg_meal_cost, address, rating) VALUES
(1, 1, 'Vasundhara Andhra Restaurant', 'Local Andhra & Vegetarian', TRUE, 180.00, 'Main Road, Araku', 4.4),
(2, 1, 'Araku Valley Bamboo Chicken & Tribal Kitchen', 'Authentic Tribal Non-Veg & Veg', FALSE, 250.00, 'Near Borra Caves junction', 4.6),
(3, 1, 'Sri Annapurna Pure Veg Tiffins', 'South Indian Pure Veg', TRUE, 120.00, 'Opposite Railway Station, Araku', 4.3),
(4, 2, 'Paradise Food Court', 'Hyderabadi Biryani & Mughlai', FALSE, 350.00, 'Secunderabad & Banjara Hills, Hyderabad', 4.5),
(5, 2, 'Chutneys', 'South Indian Vegetarian & Babai Hotel Ghee Idli', TRUE, 220.00, 'Road No 3, Banjara Hills, Hyderabad', 4.7)
ON DUPLICATE KEY UPDATE name=VALUES(name);
