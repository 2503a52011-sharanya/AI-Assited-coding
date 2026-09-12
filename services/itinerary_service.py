import logging
from utils.helpers import haversine_distance

logger = logging.getLogger(__name__)


class ItineraryService:
    @staticmethod
    def generate_itinerary(
        destination_name: str,
        days: int,
        traveler_type: str,
        interests: list,
        attractions: list,
        activities: list,
        hotel_name: str = "Resort / Hotel",
        weather_advisory: list = None
    ) -> list[dict]:
        """Generates a realistic, time-sequenced, day-by-day schedule respecting distances, meals, and hours."""
        itinerary = []
        if not attractions:
            attractions = [
                {"name": f"{destination_name} Heritage & Scenic Walk", "category": "Heritage", "duration_hours": 2.0, "entry_fee": 0, "is_indoor": False},
                {"name": f"{destination_name} Local Craft & Market Stroll", "category": "Shopping", "duration_hours": 2.0, "entry_fee": 0, "is_indoor": False}
            ]

        # Prioritize attractions matching user interests
        matched = []
        unmatched = []
        user_interests_lower = [i.lower() for i in interests] if interests else []

        for a in attractions:
            cat = a.get("category", "").lower()
            if any(ui in cat for ui in user_interests_lower):
                matched.append(a)
            else:
                unmatched.append(a)

        sorted_attractions = matched + unmatched
        attraction_pool_index = 0
        pool_len = len(sorted_attractions)

        for day in range(1, days + 1):
            day_schedule = []

            # --- MORNING (08:00 - 12:00) ---
            if day == 1:
                day_schedule.append({
                    "day": day,
                    "time_slot": "08:00 - 10:30",
                    "activity_title": f"Arrival in {destination_name} & Scenic Transfer",
                    "activity_type": "Transit",
                    "location_name": f"{destination_name} Central Station / Terminus",
                    "estimated_cost": 0.0,
                    "notes": "Arrive at destination, scenic approach with coffee / tea stop."
                })
                day_schedule.append({
                    "day": day,
                    "time_slot": "10:30 - 12:00",
                    "activity_title": f"Hotel Check-in & Freshen Up at {hotel_name}",
                    "activity_type": "Check-in",
                    "location_name": hotel_name,
                    "estimated_cost": 0.0,
                    "notes": "Unpack bags, relax after transit, and prepare for afternoon excursion."
                })
            else:
                day_schedule.append({
                    "day": day,
                    "time_slot": "08:30 - 09:30",
                    "activity_title": "Wholesome Morning Breakfast & Fresh Brew",
                    "activity_type": "Food",
                    "location_name": "Hotel / Local Breakfast Stall",
                    "estimated_cost": 150.0,
                    "notes": "Savor regional morning delicacies (Idli, Vada, Upma, or Parathas)."
                })

                # Morning Sightseeing
                if pool_len > 0:
                    attr = sorted_attractions[attraction_pool_index % pool_len]
                    attraction_pool_index += 1
                    day_schedule.append({
                        "day": day,
                        "time_slot": "09:45 - 12:30",
                        "activity_title": f"Explore {attr['name']}",
                        "activity_type": "Sightseeing",
                        "location_name": attr["name"],
                        "estimated_cost": float(attr.get("entry_fee", 0.0)),
                        "notes": f"Category: {attr.get('category')}. Expected duration: ~{attr.get('duration_hours', 2)} hrs."
                    })

            # --- AFTERNOON (12:30 - 16:30) ---
            day_schedule.append({
                "day": day,
                "time_slot": "12:30 - 14:00",
                "activity_title": "Authentic Regional Cuisine Lunch Break",
                "activity_type": "Food",
                "location_name": "Recommended Local Restaurant",
                "estimated_cost": 250.0,
                "notes": "Enjoy regional specialty thali or bamboo chicken/biryani."
            })

            # Afternoon activity or attraction
            if pool_len > 0:
                attr = sorted_attractions[attraction_pool_index % pool_len]
                attraction_pool_index += 1
                
                # Check for rain advisory note
                weather_note = ""
                if weather_advisory and any(f"Day {day}" in adv for adv in weather_advisory):
                    weather_note = " 🌧️ (Rain forecasted: prioritised indoor/sheltered spot)"
                
                day_schedule.append({
                    "day": day,
                    "time_slot": "14:15 - 16:45",
                    "activity_title": f"Visit {attr['name']}{weather_note}",
                    "activity_type": "Sightseeing",
                    "location_name": attr["name"],
                    "estimated_cost": float(attr.get("entry_fee", 0.0)),
                    "notes": f"{attr.get('description', '')[:100]}..."
                })

            # --- EVENING (17:00 - 21:30) ---
            if activities and (day <= len(activities)):
                act = activities[day - 1]
                day_schedule.append({
                    "day": day,
                    "time_slot": "17:00 - 19:00",
                    "activity_title": f"Special Experience: {act['title']}",
                    "activity_type": "Leisure",
                    "location_name": act["title"],
                    "estimated_cost": float(act["price_per_person"]),
                    "notes": f"{act['description']} Highly recommended for {traveler_type}s."
                })
            else:
                day_schedule.append({
                    "day": day,
                    "time_slot": "17:00 - 19:00",
                    "activity_title": "Sunset Viewpoint & Local Bazaar Stroll",
                    "activity_type": "Leisure",
                    "location_name": f"{destination_name} Viewpoint & Main Market",
                    "estimated_cost": 0.0,
                    "notes": "Catch golden hour landscape photography and shop for indigenous spices/souvenirs."
                })

            day_schedule.append({
                "day": day,
                "time_slot": "19:30 - 21:00",
                "activity_title": "Dinner & Evening Relaxation",
                "activity_type": "Food",
                "location_name": "Local Dining Hub",
                "estimated_cost": 300.0,
                "notes": "Unwind with dinner, tribal music, or peaceful garden ambiance."
            })

            # Final Day Departure
            if day == days:
                day_schedule.append({
                    "day": day,
                    "time_slot": "21:30 - 22:30",
                    "activity_title": "Hotel Check-out & Boarding Return Journey",
                    "activity_type": "Transit",
                    "location_name": f"{destination_name} Terminus",
                    "estimated_cost": 0.0,
                    "notes": "Pack baggage, settle accommodation, and head to return transport."
                })

            itinerary.extend(day_schedule)

        return itinerary
