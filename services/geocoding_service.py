import logging
import requests
from typing import Optional, Tuple, Dict
from config.constants import SEED_DESTINATIONS

logger = logging.getLogger(__name__)

class GeocodingService:
    """
    Geocoding service that converts location names to latitude and longitude.
    Uses cached seed coordinates first, then OpenStreetMap Nominatim.
    CRITICAL: Never invents fake coordinates. If not found, returns None.
    """
    def __init__(self):
        self._cache: Dict[str, Tuple[float, float]] = {}
        # Pre-seed known coordinates
        for dest in SEED_DESTINATIONS:
            self._cache[dest["name"].lower().strip()] = (dest["lat"], dest["lng"])

    def get_coordinates(self, location_name: str) -> Optional[Tuple[float, float]]:
        if not location_name or not location_name.strip():
            return None

        clean_name = location_name.strip().lower()
        if clean_name in self._cache:
            return self._cache[clean_name]

        # Query Nominatim API with polite headers and 2s timeout
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location_name.strip(),
                "format": "json",
                "limit": 1
            }
            headers = {
                "User-Agent": "TourismAI-Platform-Streamlit/1.0"
            }
            resp = requests.get(url, params=params, headers=headers, timeout=2.5)
            if resp.status_code == 200:
                data = resp.json()
                if data and len(data) > 0:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    self._cache[clean_name] = (lat, lon)
                    return (lat, lon)
        except Exception as e:
            logger.debug(f"Geocoding lookup failed for {location_name}: {e}")

        return None

geocoding_service = GeocodingService()
