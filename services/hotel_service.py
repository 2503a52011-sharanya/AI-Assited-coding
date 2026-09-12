import logging
from database.queries import fetch_all, get_hotels_by_destination

logger = logging.getLogger(__name__)


class HotelService:
    @staticmethod
    def search_hotels(destination_id: int, max_price: float = None, hotel_type: str = None, min_rating: float = 3.0):
        """Searches hotels for destination with filtering by price, type, and rating."""
        hotels = get_hotels_by_destination(destination_id)
        
        filtered = []
        for h in hotels:
            price = float(h["price_per_night"])
            if max_price and price > max_price:
                continue
            if hotel_type and hotel_type != "All" and h["hotel_type"].lower() != hotel_type.lower():
                continue
            if float(h["rating"]) < min_rating:
                continue
            
            filtered.append({
                "id": h["id"],
                "destination_id": h["destination_id"],
                "name": h["name"],
                "hotel_type": h["hotel_type"],
                "star_rating": h["star_rating"],
                "address": h["address"],
                "price_per_night": price,
                "amenities": [a.strip() for a in h["amenities"].split(",") if a.strip()] if h["amenities"] else ["WiFi", "Room Service"],
                "rating": float(h["rating"]),
                "image_url": h["image_url"] or "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
                "is_demo": True
            })
            
        return filtered

    @staticmethod
    def get_hotel_by_id(hotel_id: int):
        rows = fetch_all("SELECT * FROM hotels WHERE id = :hid", {"hid": hotel_id})
        return rows[0] if rows else None
