import math
from datetime import datetime, timedelta
from typing import Dict, Any, List
from config.constants import SEED_DESTINATIONS, CURRENCIES
from services.currency_service import currency_service
from services.hotel_service import hotel_service
from services.restaurant_service import restaurant_service
from services.transport_service import transport_service

class RecommendationEngine:
    """
    Intelligent algorithmic and curated recommendation engine.
    Acts as the robust fallback when Gemini API key is missing or offline.
    Supports ANY global destination with rich day-by-day itineraries.
    """

    @staticmethod
    def generate_recommendation(
        start_location: str,
        destination: str,
        start_date: str,
        end_date: str,
        days: int,
        travelers: int,
        budget: float,
        currency: str,
        travel_style: str,
        interests: List[str],
        accommodation_pref: str,
        food_preferences: List[str],
        transport_preferences: List[str],
        weather_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Determine destination profile (look up seed or construct dynamic)
        seed_match = next((d for d in SEED_DESTINATIONS if d["name"].lower() == destination.lower().strip()), None)
        
        dest_summary = (
            seed_match["description"] if seed_match else
            f"{destination} is a captivating travel destination, offering rich local culture, distinctive architecture, scenic sights, and authentic regional culinary traditions."
        )

        attractions_pool = seed_match["top_attractions"] if seed_match else [
            f"Historic Old Quarter & Heritage Square in {destination}",
            f"{destination} Central Cultural Museum & Art Pavilion",
            f"Scenic Viewpoint & Sunset Overlook of {destination}",
            f"Bustling Artisan Market & Local Handicrafts Bazaar",
            f"Iconic Waterfront Promenade / Botanical Gardens of {destination}",
            f"Historic Fortress & Architectural Citadel",
            f"Renowned Culinary Street & Evening Night Market"
        ]

        # 1. Build Day-by-Day Timeline Itinerary
        itinerary = []
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        except Exception:
            start_dt = datetime.now()

        # Adjust activities based on weather
        is_rainy = weather_info.get("is_rainy", False)
        
        for d in range(1, days + 1):
            cur_date = (start_dt + timedelta(days=d - 1)).strftime("%Y-%m-%d")
            attr_1 = attractions_pool[(d * 2 - 2) % len(attractions_pool)]
            attr_2 = attractions_pool[(d * 2 - 1) % len(attractions_pool)]
            
            theme = f"Day {d}: Immersion in {destination} Heritage & Highlights" if d == 1 else (
                f"Day {d}: Cultural Exploration & Vibrant Markets" if d % 2 == 0 else
                f"Day {d}: Scenic Vistas & Regional Gastronomy"
            )

            # Weather influence
            if is_rainy and d == 1:
                morning_act = f"Indoor Tour: {attr_1} and Heritage Gallery"
                morning_desc = "Focused on sheltered indoor exhibits due to forecast rain showers."
            else:
                morning_act = f"Guided Walking Discovery of {attr_1}"
                morning_desc = "Explore the architecture, photography angles, and landmark history."

            afternoon_act = f"Visit {attr_2} and Artisan Quarter"
            evening_act = f"Sunset Promenade and Traditional Dinner Experience in {destination}"

            itinerary.append({
                "day": d,
                "date": cur_date,
                "theme": theme,
                "morning": {
                    "time": "09:00 AM - 12:30 PM",
                    "activity": morning_act,
                    "location": f"Central District, {destination}",
                    "duration": "3.5 hours",
                    "travel_time": "20 mins",
                    "estimated_cost": int(300 * CurrencyService_multiplier(currency)),
                    "meal_recommendation": f"Traditional breakfast with local artisanal tea/coffee near {attr_1}"
                },
                "afternoon": {
                    "time": "01:30 PM - 05:00 PM",
                    "activity": afternoon_act,
                    "location": f"Cultural Belt, {destination}",
                    "duration": "3.5 hours",
                    "travel_time": "15 mins",
                    "estimated_cost": int(450 * CurrencyService_multiplier(currency)),
                    "meal_recommendation": f"Signature lunch featuring {food_preferences[0] if food_preferences else 'Local Specialties'}"
                },
                "evening": {
                    "time": "06:00 PM - 09:30 PM",
                    "activity": evening_act,
                    "location": f"Scenic Riverside / Promenade, {destination}",
                    "duration": "3.5 hours",
                    "travel_time": "25 mins",
                    "estimated_cost": int(600 * CurrencyService_multiplier(currency)),
                    "meal_recommendation": "Atmospheric rooftop dining enjoying local music and regional dishes"
                }
            })

        # 2. Hotels & Stays
        hotels = hotel_service.get_hotels_for_trip(
            destination=destination,
            days=days,
            travelers=travelers,
            travel_style=travel_style,
            accommodation_pref=accommodation_pref,
            currency=currency
        )
        selected_hotel = hotels[0] if hotels else {}
        est_hotel_cost = selected_hotel.get("total_estimated_price", 10000)

        # 3. Dining & Restaurants
        restaurants = restaurant_service.get_restaurants_for_trip(
            destination=destination,
            food_preferences=food_preferences,
            currency=currency
        )
        avg_meal_cost = restaurants[0].get("avg_cost_converted", 500) if restaurants else 500
        est_food_cost = avg_meal_cost * 3 * days * travelers

        # 4. Transportation
        trans_options = transport_service.get_transport_options(
            start_location=start_location,
            destination=destination,
            travelers=travelers,
            currency=currency
        )
        # Select first realistic transport option matching preference
        pref_lower = [t.lower() for t in transport_preferences]
        chosen_transport = trans_options[0]
        for t in trans_options:
            if any(p in t["type"].lower() for p in pref_lower):
                chosen_transport = t
                break
        est_transport_cost = chosen_transport.get("total_cost_converted", 4500)

        # 5. Local Activities & Sightseeing
        est_activity_cost = sum(
            day["morning"]["estimated_cost"] + day["afternoon"]["estimated_cost"]
            for day in itinerary
        ) * travelers
        est_local_travel = int((days * 400 * travelers) * CurrencyService_multiplier(currency))
        est_misc = int((days * 250 * travelers) * CurrencyService_multiplier(currency))

        total_estimated = round(
            est_hotel_cost + est_food_cost + est_transport_cost +
            est_activity_cost + est_local_travel + est_misc, 2
        )

        # 6. Budget Analysis & Alternatives
        remaining = round(budget - total_estimated, 2)
        utilization = round((total_estimated / budget) * 100, 1) if budget > 0 else 100
        is_over = total_estimated > budget

        alternatives = []
        if is_over:
            alternatives = [
                {
                    "category": "Accommodation",
                    "original": f"{accommodation_pref} (Est. {currency_service.format_currency(est_hotel_cost, currency)})",
                    "suggestion": "Opt for highly-rated 3-Star Boutique or Heritage Homestay",
                    "potential_savings": currency_service.format_currency(est_hotel_cost * 0.35, currency)
                },
                {
                    "category": "Transportation",
                    "original": f"{chosen_transport['type']} (Est. {currency_service.format_currency(est_transport_cost, currency)})",
                    "suggestion": "Switch to Express AC Rail or Shared Executive Shuttle",
                    "potential_savings": currency_service.format_currency(est_transport_cost * 0.45, currency)
                },
                {
                    "category": "Dining & Food",
                    "original": f"Full-service dining (Est. {currency_service.format_currency(est_food_cost, currency)})",
                    "suggestion": "Mix curated local food trails and street markets with select fine dining",
                    "potential_savings": currency_service.format_currency(est_food_cost * 0.25, currency)
                }
            ]

        # 7. Travel Tips
        travel_tips = [
            f"Pre-book major heritage entries in {destination} online to skip long ticketing queues.",
            f"Peak daylight hours in {destination} are best spent exploring indoor architecture or sheltered galleries.",
            "Always retain digital copies of transport boarding passes and government photo identification.",
            "Tipping around 7-10% at sit-down restaurants is customary and appreciated by hospitality staff."
        ]
        if weather_info.get("advice"):
            travel_tips.insert(0, f"Weather Note: {weather_info['advice']}")

        return {
            "destination_summary": dest_summary,
            "attractions": attractions_pool[:6],
            "hotels": hotels,
            "restaurants": restaurants,
            "transport_options": trans_options,
            "weather_advice": weather_info.get("advice", "Pack comfortable walking shoes and weather-appropriate attire."),
            "itinerary": itinerary,
            "estimated_costs": {
                "transportation": round(est_transport_cost, 2),
                "accommodation": round(est_hotel_cost, 2),
                "food": round(est_food_cost, 2),
                "activities": round(est_activity_cost, 2),
                "local_travel": round(est_local_travel, 2),
                "miscellaneous": round(est_misc, 2),
                "total_estimated": total_estimated,
                "currency": currency
            },
            "budget_analysis": {
                "total_budget": budget,
                "estimated_cost": total_estimated,
                "remaining_budget": remaining,
                "utilization_percentage": utilization,
                "status": "Over Budget - AI Alternatives Available" if is_over else "Within Budget",
                "is_over_budget": is_over,
                "alternatives": alternatives
            },
            "travel_tips": travel_tips
        }

def CurrencyService_multiplier(currency: str) -> float:
    rate = currency_service.get_rate_to_inr(currency)
    return 1.0 / rate if rate > 0 else 1.0

recommendation_engine = RecommendationEngine()
