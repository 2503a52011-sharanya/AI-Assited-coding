import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI SMART TOURISM & TRAVEL RECOMMENDATION SYSTEM"
    TAGLINE: str = "Your Journey. Your Interests. Your AI-Powered Trip."
    SUBTITLE: str = "Plan smarter. Travel better. Stay within your budget."
    VERSION: str = "1.0.0"

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "").strip()
    PLACES_API_KEY: str = os.getenv("PLACES_API_KEY", "").strip()
    MAPS_API_KEY: str = os.getenv("MAPS_API_KEY", "").strip()
    CURRENCY_API_KEY: str = os.getenv("CURRENCY_API_KEY", "").strip()

    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/tourism_ai").strip()
    DATABASE_NAME: str = "tourism_ai"

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_jwt_key_tourism_ai_2026").strip()

    # Pre-seeded admin user
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@tourism.ai").strip()
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin@12345").strip()

    @classmethod
    def has_gemini_key(cls) -> bool:
        return bool(cls.GEMINI_API_KEY and len(cls.GEMINI_API_KEY) > 10)

    @classmethod
    def has_weather_key(cls) -> bool:
        return bool(cls.WEATHER_API_KEY and len(cls.WEATHER_API_KEY) > 5)

settings = Settings()
