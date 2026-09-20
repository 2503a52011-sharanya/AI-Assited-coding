from typing import List, Dict, Any, Optional
from database.repositories import Repository
from services.currency_service import currency_service

class RestaurantService:
    @staticmethod
    def get_restaurants_for_trip(
        destination: str,
        food_preferences: Optional[List[str]] = None,
        currency: str = "INR"
    ) -> List[Dict[str, Any]]:
        # Query DB first
        rests = Repository.list_restaurants(destination=destination)
        
        if not rests:
            # Fallback dynamic restaurants for custom destination
            primary_food = food_preferences[0] if food_preferences else "Local Food"
            rests = [
                {
                    "_id": f"rst-gen-1-{destination.lower()[:4]}",
                    "name": f"The Spice & Soul Bistro",
                    "destination": destination,
                    "cuisine": f"Authentic {destination} Cuisine",
                    "price_level": "$$",
                    "avg_cost_per_person": 750,
                    "rating": 4.8,
                    "opening_hours": "11:30 AM - 11:00 PM",
                    "food_type": primary_food,
                    "address": f"Historic Bazaar Road, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
                    "description": f"Award-winning dining house presenting celebrated traditional flavors of {destination}."
                },
                {
                    "_id": f"rst-gen-2-{destination.lower()[:4]}",
                    "name": f"{destination} Street Flavor Market",
                    "destination": destination,
                    "cuisine": "Street Food & Quick Bites",
                    "price_level": "$",
                    "avg_cost_per_person": 350,
                    "rating": 4.6,
                    "opening_hours": "04:00 PM - 11:30 PM",
                    "food_type": "Street Food",
                    "address": f"Clock Tower Square, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80",
                    "description": f"Vibrant culinary hotspot known for authentic savory street snacks and fragrant sweets."
                },
                {
                    "_id": f"rst-gen-3-{destination.lower()[:4]}",
                    "name": f"Skyline Artisanal Terrace",
                    "destination": destination,
                    "cuisine": "Fine Dining & Continental",
                    "price_level": "$$$",
                    "avg_cost_per_person": 1800,
                    "rating": 4.9,
                    "opening_hours": "06:30 PM - 12:00 AM",
                    "food_type": "Fine Dining",
                    "address": f"High Ridge Plaza, {destination}",
                    "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
                    "description": f"Candlelit rooftop restaurant boasting scenic panoramic views of {destination}."
                }
            ]

        # Convert costs to trip currency
        for r in rests:
            base_inr = float(r.get("avg_cost_per_person", 600))
            r["avg_cost_converted"] = currency_service.convert(base_inr, "INR", currency)
            r["currency"] = currency

        return rests

restaurant_service = RestaurantService()
