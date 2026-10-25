# AI Smart Travel and Tourism Recommendation System
> **“Your Journey. Your Interests. Your AI-Powered Trip.”**

A complete, modern, responsive full-stack web application designed for intelligent tourism. It features personalized AI-driven itinerary generation, real-time satellite weather tracking, automated weather-aware itinerary adjustment with side-by-side revision reviews, a conversational travel assistant powered by the Google Gemini API, and unified in-platform bookings for hotels, intercity transit, and sightseeing activities with Razorpay payment processing.

---

## 🌟 Key Features

1. **Smart AI Trip Planner**:
   - Dynamic itinerary generation based on starting location, destination, departure/return dates, number of travelers, budget (in ₹ INR), and travel styles (Family, Heritage, Nature, Adventure, Relaxation, etc.).
   - Realistic morning, afternoon, and evening attraction pacing with estimated distances, costs, and remaining budget tracking.

2. **Real-Time Weather Integration & Radar**:
   - Live OpenWeather satellite feed for temperatures, conditions, humidity, wind speeds, and 5-day forecasts.
   - Clear live vs demo mode transparency badges.

3. **Automatic Weather-Based Itinerary Adjustment**:
   - Detects unfavorable forecast conditions (rain, thunderstorms, severe weather) impacting planned outdoor activities.
   - Automatically suggests indoor cultural, museum, or sheltered alternatives from the destination catalog.
   - Displays a side-by-side comparison of original vs proposed activities, cost differences, and rationale.
   - Requires traveler approval before updating the saved itinerary.

4. **Interactive Leaflet & OpenStreetMap Routing**:
   - Sequential itinerary markers with customized numbers.
   - Start location, hotel node, and connected route waypoints.
   - Two-way click synchronization between map pins and attraction cards.

5. **AI Travel Chatbot (Google Gemini API)**:
   - Conversational assistant embedded in a floating widget across all pages.
   - Context-aware answers regarding budgets, kids-friendly spots, weather forecasts, and the authenticated user's private bookings.
   - Built-in rule-based fallback assistant when Gemini API keys are absent or quotas are exceeded.

6. **All-in-One Booking Engine**:
   - Hotel room reservations with check-in/out date calculations.
   - Transit bookings (cabs, AC buses) with seat availability.
   - Sightseeing activities & tours with time-slot management.
   - Concurrency protection: Atomic database transactions and `select_for_update()` row-level locking to prevent overbooking.
   - Unified checkout with Razorpay test mode payment verification and printable vouchers with QR representation.

7. **Role-Based Portals (RBAC)**:
   - **Traveler**: Plan trips, manage bookings, review weather alerts, cancel reservations.
   - **Service Provider**: Manage inventory, approve/reject traveler requests, track bookings.
   - **Platform Administrator**: Access protected administrative headquarters (`/portal-admin/dashboard/`) to moderate vendors, audit security logs, and inspect platform metrics.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.14+, Django 6.x, Django REST Framework
- **Primary Database**: MySQL 8.x (PyMySQL driver with seamless SQLite fallback)
- **Frontend**: HTML5, Tailwind CSS (via CDN), FontAwesome 6, Leaflet Maps
- **AI Engine**: Google Gemini API (`google-generativeai`)
- **Weather Service**: OpenWeather API & Climate Modeling Engine
- **Payment Processing**: Razorpay API (Test / Sandbox Mode)

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.10+ installed
- MySQL 8.x (optional; system will automatically default to SQLite if MySQL service is not running locally)

### 2. Environment Configuration
Create or modify `.env` in the root directory:
```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*

# MySQL Database
DB_ENGINE=mysql
DB_NAME=ai_smart_tourism
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

# API Integrations (Optional, demo mode available)
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
RAZORPAY_KEY_ID=rzp_test_demo123456789
RAZORPAY_KEY_SECRET=demoSecretKey987654321
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations & Seeding
```bash
python manage.py migrate
python seed_data.py
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Open your browser at `http://127.0.0.1:8000/`.

---

## 🔑 Default Seed Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Platform Administrator** | `admin` | `admin123` | System management at `/portal-admin/dashboard/` & `/admin/` |
| **Service Provider** | `provider_goa` | `provider123` | Vendor operations at `/provider/dashboard/` |
| **Traveler** | `traveler_demo` | `traveler123` | Booking, AI trip planning, and profile management |
