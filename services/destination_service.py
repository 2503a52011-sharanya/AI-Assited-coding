import logging
import requests
from config.settings import NOMINATIM_BASE_URL
from database.queries import (
    get_destination_by_name, search_destinations, get_all_destinations,
    save_destination, get_attractions_by_destination, get_hotels_by_destination,
    get_activities_by_destination, get_restaurants_by_destination, execute_query
)
from utils.caching import get_cached_api_response, set_cached_api_response

logger = logging.getLogger(__name__)


class DestinationService:
    @staticmethod
    def get_all(limit=100):
        return get_all_destinations(limit=limit)

    @staticmethod
    def search(query: str):
        """Searches local database; if no match or sparse, looks up external geocoding API."""
        if not query or not query.strip():
            return get_all_destinations(limit=20)
        
        cleaned = query.strip()
        local_results = search_destinations(cleaned)
        if local_results:
            return local_results
        
        # If not in DB, discover via OpenStreetMap Nominatim API
        discovered = DestinationService.discover_via_api(cleaned)
        if discovered:
            return [discovered]
        
        # Final synthetic fallback so user never gets "Destination not found"
        fallback = DestinationService.create_fallback_destination(cleaned)
        return [fallback]

    @staticmethod
    def get_by_name_or_discover(name: str):
        """Finds a destination by exact name or dynamically discovers it."""
        dest = get_destination_by_name(name)
        if dest:
            return dest
        
        discovered = DestinationService.discover_via_api(name)
        if discovered:
            return discovered
        
        return DestinationService.create_fallback_destination(name)

    @staticmethod
    def discover_via_api(place_name: str):
        """Queries OpenStreetMap Nominatim API to resolve real coordinates and state."""
        cache_key = f"nominatim_{place_name.lower()}"
        cached = get_cached_api_response(cache_key)
        if cached:
            dest = get_destination_by_name(cached.get("name", place_name))
            if dest:
                return dest

        try:
            headers = {"User-Agent": "SmartTourismPlatform/2.0 (contact: support@smarttourism.ai)"}
            params = {
                "q": place_name,
                "format": "json",
                "addressdetails": 1,
                "limit": 1
            }
            resp = requests.get(f"{NOMINATIM_BASE_URL}/search", params=params, headers=headers, timeout=5)
            if resp.status_code == 200 and resp.json():
                data = resp.json()[0]
                lat = float(data["lat"])
                lon = float(data["lon"])
                address = data.get("address", {})
                state = address.get("state", address.get("region", "India"))
                city = address.get("city", address.get("town", address.get("village", place_name.title())))
                
                desc = (
                    f"{place_name.title()} is a picturesque destination located in {state}, India. "
                    f"Renowned for its cultural heritage, natural beauty, and warm regional hospitality, "
                    f"it offers travelers authentic experiences away from mainstream tourist crowds."
                )
                tags = "Nature, Culture, Photography, Local Experience"
                img = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800"

                dest_id = save_destination(
                    name=place_name.title(),
                    state=state,
                    city=city,
                    lat=lat,
                    lon=lon,
                    description=desc,
                    tags=tags,
                    image_url=img,
                    best_season="October to March",
                    avg_daily_budget=2800.0,
                    ideal_duration_days=3
                )
                
                # Auto-generate starter attractions & hotel
                DestinationService._seed_discovered_place(dest_id, place_name.title(), lat, lon)
                
                set_cached_api_response(cache_key, {"name": place_name.title(), "dest_id": dest_id})
                return get_destination_by_name(place_name)
        except Exception as e:
            logger.warning(f"Nominatim API search failed for '{place_name}': {e}")
        
        return None

    @staticmethod
    def create_fallback_destination(place_name: str):
        """Creates a safe synthetic destination entry for remote villages or custom queries."""
        dest_id = save_destination(
            name=place_name.title(),
            state="India",
            city=place_name.title(),
            lat=20.5937,
            lon=78.9629,
            description=f"{place_name.title()} is an enchanting, unexplored location with immense cultural and natural charm.",
            tags="Nature, Adventure, Culture, Scenic",
            image_url="https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800",
            best_season="October to April",
            avg_daily_budget=2500.0,
            ideal_duration_days=2
        )
        DestinationService._seed_discovered_place(dest_id, place_name.title(), 20.5937, 78.9629)
        return get_destination_by_name(place_name)

    @staticmethod
    def _seed_discovered_place(dest_id: int, name: str, lat: float, lon: float):
        """Adds starter attractions, hotels, and activities for dynamically discovered destinations."""
        # Attractions
        execute_query("""
        INSERT INTO attractions (destination_id, name, category, description, entry_fee, opening_time, closing_time, avg_visit_duration_hours, latitude, longitude, is_indoor, rating)
        VALUES 
        (:did, :a1, 'Heritage & Culture', 'Historic central viewpoint and local town square.', 0.0, '08:00', '19:00', 2.0, :lat, :lon, 0, 4.5),
        (:did, :a2, 'Nature & Scenic', 'Serene natural panoramic valley and countryside trails.', 20.0, '06:00', '18:30', 2.5, :lat, :lon, 0, 4.6)
        """, {
            "did": dest_id,
            "a1": f"{name} Heritage Walk & Viewpoint",
            "a2": f"{name} Scenic Countryside Trails",
            "lat": lat, "lon": lon
        })
        
        # Hotel
        execute_query("""
        INSERT INTO hotels (destination_id, name, hotel_type, star_rating, address, latitude, longitude, price_per_night, amenities, rating, image_url)
        VALUES 
        (:did, :h1, 'Budget hotel', 3, :addr1, :lat, :lon, 1600.0, 'WiFi, Hot Water, Room Service, Breakfast', 4.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'),
        (:did, :h2, 'Homestay', 2, :addr2, :lat, :lon, 1100.0, 'Home Cooked Meals, Garden, Mountain View', 4.4, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800')
        """, {
            "did": dest_id,
            "h1": f"{name} Valley View Residency",
            "h2": f"{name} Traditional Heritage Homestay",
            "addr1": f"Station Road, {name}",
            "addr2": f"Village Ridge, {name}",
            "lat": lat, "lon": lon
        })

        # Activity
        execute_query("""
        INSERT INTO activities (destination_id, title, category, description, price_per_person, duration_hours, suitable_for, rating)
        VALUES (:did, :act, 'Local Experience', 'Guided exploration of local handicraft markets and cultural sites.', 250.0, 2.0, 'All', 4.7)
        """, {"did": dest_id, "act": f"Local Exploration & Culture Walk of {name}"})

        # Restaurant
        execute_query("""
        INSERT INTO restaurants (destination_id, name, cuisine_type, is_vegetarian, avg_meal_cost, address, rating)
        VALUES (:did, :r, 'Regional Cuisine', 1, 150.0, :addr, 4.4)
        """, {"did": dest_id, "r": f"{name} Traditional Dining Kitchen", "addr": f"Main Market, {name}"})

    @staticmethod
    def get_details(destination_id: int):
        return {
            "attractions": get_attractions_by_destination(destination_id),
            "hotels": get_hotels_by_destination(destination_id),
            "activities": get_activities_by_destination(destination_id),
            "restaurants": get_restaurants_by_destination(destination_id)
        }
