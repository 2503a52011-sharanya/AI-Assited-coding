import math
from typing import List, Dict, Any, Optional
from database.repositories import Repository
from services.currency_service import currency_service

class HotelService:
    @staticmethod
    def get_hotels_for_trip(
        destination: str,
        days: int,
        travelers: int,
        travel_style: str = "Standard",
        accommodation_pref: str = "3 Star",
        currency: str = "INR"
    ) -> List[Dict[str, Any]]:
        # Check DB first
        hotels = Repository.list_hotels(destination=destination)
        rooms_needed = max(1, math.ceil(travelers / 2))
        nights = max(1, days - 1 if days > 1 else 1)

        # Style price multipliers (base INR per night)
        price_tier = {
            "Budget Hotel": 2200,
            "Hostel": 1100,
            "3 Star": 4200,
            "4 Star": 8500,
            "5 Star": 18000,
            "Homestay": 2800
        }.get(accommodation_pref, 4500)

        if not hotels:
            # Generate tailored realistic options for custom destinations
            hotels = [
                {
                    "_id": f"htl-gen-1-{destination.lower()[:4]}",
                    "provider_id": "system",
                    "name": f"The Grand {destination} Heritage Stay",
                    "destination": destination,
                    "room_type": "Deluxe Comfort Suite",
                    "price_per_night": price_tier,
                    "star_rating": 4 if "4 Star" in accommodation_pref or "5 Star" in accommodation_pref else 3,
                    "guest_rating": 4.7,
                    "amenities": ["Complimentary High-speed WiFi", "Artisanal Breakfast", "Air Conditioning", "City View"],
                    "address": f"City Center Promenade, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
                    "description": f"Conveniently positioned in {destination}, offering serene comfort and local hospitality.",
                    "is_available": True
                },
                {
                    "_id": f"htl-gen-2-{destination.lower()[:4]}",
                    "provider_id": "system",
                    "name": f"{destination} Boutique & Spa Retreat",
                    "destination": destination,
                    "room_type": "Executive King Room",
                    "price_per_night": int(price_tier * 1.3),
                    "star_rating": 5 if "5 Star" in accommodation_pref else 4,
                    "guest_rating": 4.9,
                    "amenities": ["Heated Pool & Spa", "Panoramic Rooftop Bistro", "Fitness Center", "Airport Shuttle"],
                    "address": f"Old Quarter Heritage Lane, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
                    "description": f"Upscale retreat combining authentic {destination} aesthetics with modern luxury.",
                    "is_available": True
                },
                {
                    "_id": f"htl-gen-3-{destination.lower()[:4]}",
                    "provider_id": "system",
                    "name": f"{destination} Urban Nomad Inn",
                    "destination": destination,
                    "room_type": "Standard Queen Bed",
                    "price_per_night": max(900, int(price_tier * 0.65)),
                    "star_rating": 3,
                    "guest_rating": 4.4,
                    "amenities": ["Free Breakfast", "Co-working Lounge", "Metro Proximity"],
                    "address": f"Transit Hub Avenue, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80",
                    "description": f"Cost-effective and ultra-clean accommodation ideal for smart travelers in {destination}.",
                    "is_available": True
                }
            ]

        # Calculate estimated total price in requested currency
        for h in hotels:
            base_inr_night = float(h.get("price_per_night", 3000))
            total_inr = base_inr_night * nights * rooms_needed
            
            # Convert to trip currency
            h["price_per_night_converted"] = currency_service.convert(base_inr_night, "INR", currency)
            h["total_estimated_price"] = currency_service.convert(total_inr, "INR", currency)
            h["currency"] = currency
            h["nights"] = nights
            h["rooms_needed"] = rooms_needed
            h["budget_suitability"] = "Within Budget"

        return hotels

hotel_service = HotelService()
