-- =============================================================================
-- SMART TOURISM AND TRAVEL RECOMMENDATION SYSTEM
-- DATABASE SCHEMA DEFINITION (MySQL 8.0+ / MariaDB / Relational Standards)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS smart_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_tourism;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    role VARCHAR(20) DEFAULT 'user', -- 'user' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- 2. USER PREFERENCES TABLE
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    travel_style VARCHAR(50) DEFAULT 'Comfortable',
    preferred_budget_range VARCHAR(50) DEFAULT '₹10,000 - ₹25,000',
    preferred_transport VARCHAR(50) DEFAULT 'Train',
    preferred_accommodation VARCHAR(50) DEFAULT 'Budget hotel',
    food_preference VARCHAR(50) DEFAULT 'Local food',
    interests TEXT, -- Comma-separated or JSON list
    accessibility_requirements TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_pref (user_id)
) ENGINE=InnoDB;

-- 3. DESTINATIONS TABLE
CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) DEFAULT 'India',
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    description TEXT,
    best_season VARCHAR(100),
    ideal_duration_days INT DEFAULT 3,
    avg_daily_budget DECIMAL(10, 2) DEFAULT 3500.00,
    tags TEXT, -- e.g. "Nature, Photography, Waterfalls, Coffee"
    image_url VARCHAR(500),
    is_popular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dest_name (name),
    INDEX idx_dest_state (state)
) ENGINE=InnoDB;

-- 4. DESTINATION CATEGORIES
CREATE TABLE IF NOT EXISTS destination_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    category_name VARCHAR(60) NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_cat_name (category_name)
) ENGINE=InnoDB;

-- 5. ATTRACTIONS TABLE
CREATE TABLE IF NOT EXISTS attractions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(180) NOT NULL,
    category VARCHAR(60) NOT NULL,
    description TEXT,
    entry_fee DECIMAL(10, 2) DEFAULT 0.00,
    opening_time VARCHAR(20) DEFAULT '09:00',
    closing_time VARCHAR(20) DEFAULT '18:00',
    avg_visit_duration_hours DECIMAL(3, 1) DEFAULT 2.0,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    is_indoor BOOLEAN DEFAULT FALSE,
    rating DECIMAL(2, 1) DEFAULT 4.5,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_attraction_dest (destination_id)
) ENGINE=InnoDB;

-- 6. ACTIVITIES TABLE
CREATE TABLE IF NOT EXISTS activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    title VARCHAR(180) NOT NULL,
    category VARCHAR(60) NOT NULL,
    description TEXT,
    price_per_person DECIMAL(10, 2) NOT NULL,
    duration_hours DECIMAL(3, 1) DEFAULT 2.0,
    suitable_for VARCHAR(100) DEFAULT 'All',
    rating DECIMAL(2, 1) DEFAULT 4.7,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. HOTELS TABLE
CREATE TABLE IF NOT EXISTS hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(180) NOT NULL,
    hotel_type VARCHAR(60) DEFAULT 'Budget hotel',
    star_rating INT DEFAULT 3,
    address TEXT,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    price_per_night DECIMAL(10, 2) NOT NULL,
    amenities TEXT,
    rating DECIMAL(2, 1) DEFAULT 4.2,
    image_url VARCHAR(500),
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_hotel_dest (destination_id)
) ENGINE=InnoDB;

-- 8. ROOMS TABLE
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    room_type VARCHAR(80) NOT NULL,
    capacity INT DEFAULT 2,
    price_per_night DECIMAL(10, 2) NOT NULL,
    available_count INT DEFAULT 5,
    amenities TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. RESTAURANTS TABLE
CREATE TABLE IF NOT EXISTS restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(180) NOT NULL,
    cuisine_type VARCHAR(80) NOT NULL,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    avg_meal_cost DECIMAL(10, 2) DEFAULT 300.00,
    address TEXT,
    rating DECIMAL(2, 1) DEFAULT 4.3,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. TRANSPORT PROVIDERS
CREATE TABLE IF NOT EXISTS transport_providers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    type VARCHAR(40) NOT NULL, -- Flight, Train, Bus, Cab
    code VARCHAR(30),
    contact_phone VARCHAR(40)
) ENGINE=InnoDB;

-- 11. TRANSPORT OPTIONS
CREATE TABLE IF NOT EXISTS transport_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider_id INT,
    transport_type VARCHAR(40) NOT NULL, -- Flight, Train, Bus, Cab
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    carrier_name VARCHAR(120) NOT NULL,
    service_number VARCHAR(50),
    departure_time VARCHAR(20) NOT NULL,
    arrival_time VARCHAR(20) NOT NULL,
    duration_hours DECIMAL(4, 2) NOT NULL,
    fare_economy DECIMAL(10, 2) NOT NULL,
    fare_premium DECIMAL(10, 2) DEFAULT 0.00,
    available_seats INT DEFAULT 40,
    cancellation_policy TEXT,
    FOREIGN KEY (provider_id) REFERENCES transport_providers(id) ON DELETE SET NULL,
    INDEX idx_route (origin, destination)
) ENGINE=InnoDB;

-- 12. TRIPS TABLE
CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    trip_name VARCHAR(180) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days INT NOT NULL,
    travelers_count INT NOT NULL DEFAULT 1,
    traveler_type VARCHAR(40) DEFAULT 'Solo',
    travel_style VARCHAR(40) DEFAULT 'Comfortable',
    allocated_budget DECIMAL(10, 2) NOT NULL,
    total_estimated_cost DECIMAL(10, 2) NOT NULL,
    status VARCHAR(40) DEFAULT 'Planned', -- Planned, Confirmed, Completed, Cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_trip_user (user_id)
) ENGINE=InnoDB;

-- 13. ITINERARIES TABLE
CREATE TABLE IF NOT EXISTS itineraries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 14. ITINERARY ITEMS TABLE
CREATE TABLE IF NOT EXISTS itinerary_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    itinerary_id INT NOT NULL,
    day_number INT NOT NULL,
    time_slot VARCHAR(30) NOT NULL, -- e.g. "09:00 - 11:30"
    activity_title VARCHAR(180) NOT NULL,
    activity_type VARCHAR(50) NOT NULL, -- Sightseeing, Food, Transit, Leisure, Check-in
    location_name VARCHAR(150),
    estimated_cost DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 15. BUDGETS TABLE
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    transport_cost DECIMAL(10, 2) DEFAULT 0.00,
    accommodation_cost DECIMAL(10, 2) DEFAULT 0.00,
    food_cost DECIMAL(10, 2) DEFAULT 0.00,
    activities_cost DECIMAL(10, 2) DEFAULT 0.00,
    local_transport_cost DECIMAL(10, 2) DEFAULT 0.00,
    buffer_cost DECIMAL(10, 2) DEFAULT 0.00,
    total_cost DECIMAL(10, 2) DEFAULT 0.00,
    is_optimized BOOLEAN DEFAULT FALSE,
    savings_achieved DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 16. BOOKINGS TABLE
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    trip_id INT,
    booking_reference VARCHAR(60) NOT NULL UNIQUE,
    category VARCHAR(40) NOT NULL, -- Flight, Train, Bus, Hotel, Cab, Activity
    provider_name VARCHAR(120) NOT NULL,
    item_title VARCHAR(180) NOT NULL,
    booking_date DATE NOT NULL,
    travel_date DATE NOT NULL,
    passenger_count INT DEFAULT 1,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(40) DEFAULT 'Confirmed', -- Confirmed, Cancelled, Completed, Pending
    is_demo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL,
    INDEX idx_booking_user (user_id),
    INDEX idx_booking_ref (booking_reference)
) ENGINE=InnoDB;

-- 17. BOOKING ITEMS TABLE
CREATE TABLE IF NOT EXISTS booking_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    passenger_name VARCHAR(120) NOT NULL,
    passenger_age INT,
    seat_or_room VARCHAR(40),
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 18. PAYMENTS TABLE
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    payment_reference VARCHAR(80) NOT NULL UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    payment_method VARCHAR(40) DEFAULT 'DEMO_GATEWAY',
    payment_status VARCHAR(40) DEFAULT 'SUCCESS', -- SUCCESS, FAILED, REFUNDED
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 19. REVIEWS TABLE
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    destination_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 20. RECOMMENDATIONS CACHE TABLE
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    destination_id INT NOT NULL,
    score DECIMAL(5, 2) NOT NULL,
    reasons TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 21. WEATHER CACHE TABLE
CREATE TABLE IF NOT EXISTS weather_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_name VARCHAR(150) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    weather_json TEXT NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_weather_dest (destination_name)
) ENGINE=InnoDB;

-- 22. API CACHE TABLE
CREATE TABLE IF NOT EXISTS api_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cache_key VARCHAR(255) NOT NULL UNIQUE,
    response_json MEDIUMTEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    INDEX idx_cache_key (cache_key)
) ENGINE=InnoDB;

-- 23. NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 24. ADMIN USERS TABLE
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    role VARCHAR(40) DEFAULT 'SUPER_ADMIN',
    permissions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 25. AUDIT LOGS TABLE
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
