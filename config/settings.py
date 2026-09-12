import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# App Metadata
APP_NAME = "AI-Powered Smart Tourism and Travel Recommendation System"
APP_TAGLINE = "Your Single-Window Smart Travel Assistant"
VERSION = "2.0.0"
DEFAULT_CURRENCY = "INR"
CURRENCY_SYMBOL = "₹"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smart_tourism.db")
SECRET_KEY = os.getenv("SECRET_KEY", "smart_tourism_default_secret_key_change_me")

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
MAP_API_KEY = os.getenv("MAP_API_KEY", "")
FLIGHT_API_KEY = os.getenv("FLIGHT_API_KEY", "")
HOTEL_API_KEY = os.getenv("HOTEL_API_KEY", "")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY", "")
PAYMENT_SECRET = os.getenv("PAYMENT_SECRET", "")

# External Endpoints
OPENMETEO_BASE_URL = os.getenv("OPENMETEO_BASE_URL", "https://api.open-meteo.com/v1")
NOMINATIM_BASE_URL = os.getenv("NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org")

# Operational Modes
DEMO_MODE_FLIGHTS = not bool(FLIGHT_API_KEY)
DEMO_MODE_HOTELS = not bool(HOTEL_API_KEY)
DEMO_MODE_PAYMENTS = not bool(PAYMENT_API_KEY and PAYMENT_SECRET)

# Travel Taxonomy Constants
TRAVELER_TYPES = ["Solo", "Couple", "Family", "Friends", "Business", "Group"]
TRAVEL_STYLES = ["Budget", "Economy", "Comfortable", "Luxury", "Backpacker"]
TRANSPORT_TYPES = ["Bus", "Train", "Flight", "Cab", "Rental vehicle", "Own vehicle"]
ACCOMMODATION_TYPES = ["Hostel", "Budget hotel", "2-star", "3-star", "4-star", "5-star", "Homestay", "Resort"]
FOOD_PREFERENCES = ["Vegetarian", "Non-vegetarian", "Vegan", "Local food", "Budget food", "Premium restaurants"]

INTEREST_CATEGORIES = [
    "Nature", "Adventure", "History", "Culture", "Beaches", "Mountains",
    "Wildlife", "Food", "Shopping", "Photography", "Religious", "Nightlife",
    "Family", "Romantic", "Architecture", "Museums", "Sports"
]
