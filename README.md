# AI-Powered Smart Tourism and Travel Recommendation System

A fully-featured, production-ready travel planning and tourism management platform built with **Python & Streamlit**. The platform serves as a unified, single-window assistant that enables travelers to discover destinations (from major metro hubs to remote rural villages), generate customized day-by-day itineraries, compare multi-modal transport options, book hotels and activities, optimize budgets automatically, and manage trips and digital boarding passes.

---

## 🌟 Key Features

1. **Dynamic Destination Discovery (No Hard-coded Limits)**:
   - Search for **any** village, town, district, hill station, or city (e.g. *Araku Valley, Warangal, Ooty, Hampi, Ziro, Gokarna, Munnar*).
   - Multi-tier resolution: Database cache ➔ OpenStreetMap Nominatim geocoder ➔ Dynamic synthesis with auto-caching.
   - Intelligent fallback prevents "Destination not found" errors.

2. **Personalized Multi-Factor Recommendation Engine**:
   - Transparent multi-criteria scoring algorithm based on user travel style, interests (Nature, Photography, Adventure, etc.), budget, season, and group type (Solo, Couple, Family, Friends).

3. **Budget Calculation & Automatic Optimization**:
   - Calculates itemized expenses: Transportation + Hotel + Food + Activities + Local Transit + Emergency buffer (7%).
   - Interactive breakdown charts (Plotly).
   - If estimated costs exceed user budget, the engine automatically calculates and suggests a **Smart Optimized Plan** side-by-side with exact savings!

4. **Day-by-Day Itinerary Planner**:
   - Generates morning, afternoon, and evening schedules.
   - Respects attraction opening hours, visit duration, transit times, and dining breaks.
   - Integrates live weather forecasts (via Open-Meteo) and flags rainy forecast days with indoor alternatives.

5. **Integrated In-App Booking & Digital Passes**:
   - Direct in-app booking for Trains (IRCTC-style), Buses, Flights, Outstation Cabs, Hotels, and Activity tickets.
   - Secure simulated payment checkout flow.
   - Generates official digital boarding passes and tickets with unique PNRs / booking references.

6. **Unified Management**:
   - **My Trips**: Day-by-day schedule viewer and downloadable trip summaries.
   - **My Bookings**: Real-time status, digital tickets, and cancellation workflow.
   - **Profile**: Customize travel preferences, style, budget range, and accessibility requirements.
   - **Admin Dashboard**: Catalog management, transaction metrics, and audit logs.
   - **Embedded AI Travel Assistant**: Conversational assistant answering natural queries grounded in real database pricing.

---

## 🏗️ System Architecture & Directory Structure

```text
smart-tourism/
├── app.py                     # Main entry point, session router, global styling & AI assistant
├── requirements.txt           # Project dependencies
├── .env                       # Local environment variables
├── .env.example               # Template environment configuration
├── README.md                  # Detailed documentation
│
├── config/
│   ├── settings.py            # Global constants, taxonomy, and environment loading
│   └── database.py            # Database engine with dual MySQL & SQLite fallback
│
├── database/
│   ├── schema.sql             # Full production MySQL 8.0 relational schema (25 tables)
│   ├── seed.sql               # Seed dataset for Indian destinations, hotels, transport, activities
│   └── queries.py             # SQL repository methods and auto-migration
│
├── models/
│   ├── user.py                # User and Preferences dataclasses
│   ├── destination.py         # Destination, Attraction, Hotel, Activity dataclasses
│   ├── trip.py                # Trip, ItineraryItem, and Budget dataclasses
│   ├── booking.py             # Booking and BookingItem dataclasses
│   └── recommendation.py      # RecommendationScore dataclass
│
├── services/
│   ├── destination_service.py # Dynamic geocoding, OpenStreetMap discovery & DB fallback
│   ├── weather_service.py     # Live Open-Meteo weather integration & rain alerts
│   ├── flight_service.py      # Multi-tier flight search & sorting (Cheapest, Fastest, Value)
│   ├── train_service.py       # IRCTC train schedules, seat classes (1A, 2A, 3A, SL)
│   ├── bus_service.py         # Bus booking (State RTCs, Volvo AC Sleepers)
│   ├── hotel_service.py       # Lodging catalog, filters, and rates
│   ├── activity_service.py    # Attractions, tours, and entrance ticket services
│   ├── map_service.py         # Coordinate distance math, PyDeck map data generation
│   ├── itinerary_service.py   # Day-by-day scheduler respecting meals, hours, and distances
│   ├── budget_service.py      # Budget breakdown math & auto-optimization engine
│   ├── recommendation_service.py # Multi-criteria weighted recommendation scoring
│   ├── payment_service.py     # Payment gateway abstraction & demo verification
│   ├── booking_service.py     # In-app reservation workflow & ticket persistence
│   └── ai_assistant_service.py# Natural language assistant powered by database data
│
├── pages/
│   ├── home.py                # Hero landing page, smart search, quick tools
│   ├── explore.py             # Multi-faceted destination explorer with filters
│   ├── planner.py             # "Plan My Trip" personalized journey wizard
│   ├── destinations.py        # Detailed spotlight, weather forecast & amenities
│   ├── transportation.py      # Search & book Flights, Trains, Buses, Cabs
│   ├── hotels.py              # Hotel discovery, amenities, and room booking
│   ├── activities.py          # Sightseeing passes & experiences
│   ├── budget.py              # Standalone budget calculator & comparison simulator
│   ├── trips.py               # "My Trips" dashboard & itinerary download
│   ├── bookings.py            # "My Bookings" with digital boarding passes
│   ├── profile.py             # User profile & smart preference configuration
│   └── admin.py               # Admin CMS, platform KPIs, revenue, audit logs
│
└── tests/
    ├── test_auth.py           # Unit tests for password hashing and validation
    ├── test_budget.py         # Unit tests for budget math and auto-optimization
    ├── test_itinerary.py      # Unit tests for itinerary sequencing
    ├── test_recommendations.py# Unit tests for scoring engine
    ├── test_destinations.py   # Unit tests for geocoding & fallbacks
    ├── test_bookings.py       # Unit tests for booking workflows
    └── test_scenario_39.py    # End-to-end test for Section 39 requirements
```

---

## 🚀 Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10 to 3.14 installed.
- (Optional) MySQL Server 8.0+ if you wish to run MySQL instead of SQLite.

### 2. Environment Setup
Clone or navigate to the project directory:
```bash
cd "c:\Users\DELL\OneDrive\ai_assted coding"
```

Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### 3. Database Setup

#### Option A: Zero-Config SQLite (Default Out of the Box)
The application is preconfigured to use SQLite by default (`DATABASE_URL=sqlite:///smart_tourism.db`). On first launch, it automatically creates all 25 tables and seeds realistic Indian destinations, hotels, trains, buses, and activities. **No manual DB setup is required!**

#### Option B: Production MySQL
If you want to use MySQL:
1. Log into your MySQL console:
   ```sql
   CREATE DATABASE smart_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   USE smart_tourism;
   SOURCE database/schema.sql;
   SOURCE database/seed.sql;
   ```
2. Edit `.env`:
   ```ini
   DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/smart_tourism
   ```

---

### 4. Running the Web Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

### 5. Running Automated Tests
Run the test suite using `pytest`:
```bash
python -m pytest tests/ -v
```
All 10 test suites, including the Section 39 scenario test, will execute and validate:
- Authentication and PBKDF2 hashing
- Dynamic OpenStreetMap location discovery
- Recommendation scoring algorithm
- Day-by-day itinerary generation
- Budget auto-optimization and savings calculation
- End-to-end booking flow and digital ticket issuance

---

## 🧪 Section 39 Verification Scenario

To test the specific scenario described in Section 39:
1. Navigate to **Plan My Trip** in the sidebar.
2. Set:
   - **Origin**: `Hyderabad`
   - **Destination**: `Araku Valley`
   - **Travelers**: `2`
   - **Days**: `3`
   - **Traveler Type**: `Couple`
   - **Budget**: `₹20,000`
   - **Interests**: `Nature` + `Photography`
   - **Transport**: `Train + Local Cab`
   - **Accommodation**: `Budget hotel`
   - **Food**: `Local food / Vegetarian`
3. Click **Generate Personalized Travel Plan**.
4. Review the generated 3-day itinerary, live weather forecast, and budget comparison.
5. Click **Confirm & Book Package** in the checkout tab.
6. Check **My Trips** to download the summary and **My Bookings** to view the digital tickets!

---

## 🔒 Security & Credentials Handling
- API keys are managed through `.env` and loaded via `python-dotenv`.
- In the absence of third-party API credentials, the platform seamlessly operates in **Verified Demo Mode**.
- User passwords are encrypted using PBKDF2 with SHA-256 HMAC and salt.
- Credit card and banking credentials are never stored in plain text.
