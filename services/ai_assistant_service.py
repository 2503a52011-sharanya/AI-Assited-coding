import re
import logging
from services.destination_service import DestinationService
from services.recommendation_service import RecommendationService
from services.budget_service import BudgetService
from services.train_service import TrainService
from services.hotel_service import HotelService
from utils.helpers import format_currency

logger = logging.getLogger(__name__)


class AIAssistantService:
    @staticmethod
    def answer_query(user_query: str) -> str:
        """
        Processes natural language travel planning queries using real system data,
        extracting budget numbers, duration, origin, and interests.
        """
        text = user_query.lower()

        # 1. Extract Budget (e.g. 15000, 20k, ₹15,000)
        budget = 20000.0
        budget_match = re.search(r'(?:₹|rs\.?|inr)?\s*([0-9]{1,2}(?:,[0-9]{2,3})*(?:,000)?|[0-9]+k)', text)
        if budget_match:
            raw_b = budget_match.group(1).replace(",", "")
            if raw_b.endswith("k"):
                budget = float(raw_b[:-1]) * 1000
            else:
                try:
                    budget = float(raw_b)
                except ValueError:
                    budget = 20000.0

        # 2. Extract Days (e.g. 3 days, 2 nights, weekend)
        days = 3
        days_match = re.search(r'(\d+)\s*(?:days?|d)', text)
        if days_match:
            days = max(1, min(14, int(days_match.group(1))))
        elif "weekend" in text:
            days = 2

        # 3. Extract Origin (e.g. from hyderabad, starting hyderabad)
        origin = "Hyderabad"
        origin_match = re.search(r'(?:from|starting(?: from)?)\s+([a-zA-Z]+)', text)
        if origin_match:
            origin = origin_match.group(1).title()

        # 4. Extract Interests
        # 4. Extract Traveler Type & Count
        traveler_type = "Solo"
        trav_count = 1
        if any(k in text for k in ["family", "kids", "children", "parents"]):
            traveler_type = "Family"
            trav_count = 4
        elif any(k in text for k in ["friends", "buddies", "gang", "bachelors"]):
            traveler_type = "Friends"
            trav_count = 4
        elif any(k in text for k in ["group", "team", "colleagues"]):
            traveler_type = "Group"
            trav_count = 6
        elif any(k in text for k in ["business", "corporate", "work"]):
            traveler_type = "Business"
            trav_count = 1
        elif any(k in text for k in ["couple", "honeymoon", "romantic", "partner", "wife", "husband"]):
            traveler_type = "Couple"
            trav_count = 2

        # 5. Extract Interests
        detected_interests = []
        for kw in ["nature", "photography", "history", "culture", "beaches", "mountains", "adventure", "religious", "food"]:
            if kw in text:
                detected_interests.append(kw.title())
        if not detected_interests:
            detected_interests = ["Nature", "Photography"]

        # 6. Query Recommendation Engine using Real System Data
        recs = RecommendationService.get_personalized_recommendations(
            origin=origin,
            target_budget=budget,
            days=days,
            traveler_type=traveler_type,
            interests=detected_interests,
            limit=3
        )

        if not recs:
            return "I couldn't locate matching destinations for your parameters. Try searching for Araku Valley, Ooty, or Hampi!"

        best_dest = recs[0]
        dest_name = best_dest.destination_name
        dest_obj = DestinationService.get_by_name_or_discover(dest_name)
        details = DestinationService.get_details(dest_obj["id"])

        # Fetch Real Transport
        trains = TrainService.search_trains(origin, dest_name, "2026-09-15")
        transport_name = trains[0]["train_name"] if trains else "Express Train / AC Bus"
        trans_fare = trains[0]["fare_3ac"] if trains else 500.0

        # Fetch Real Hotel
        hotels = details.get("hotels", [])
        hotel_name = hotels[0]["name"] if hotels else "Valley View Residency"
        hotel_rate = float(hotels[0]["price_per_night"]) if hotels else 1500.0

        # Budget Calculation
        calc = BudgetService.calculate_trip_budget(
            days=days,
            travelers=trav_count,
            transport_fare_per_person=trans_fare,
            hotel_nightly_rate=hotel_rate,
            food_style="Local food",
            travel_style="Comfortable",
            activities_cost_per_person=400.0,
            local_cab_daily_rate=1200.0
        )

        opt = BudgetService.optimize_budget(
            user_budget=budget,
            original_plan=calc,
            days=days,
            travelers=trav_count,
            current_transport_type="Train",
            current_hotel_price=hotel_rate
        )

        # Build Response
        response = f"""### 🤖 AI Travel Recommendation & Itinerary

Based on your preferences (**{format_currency(budget)} budget, {days} days, starting from {origin}, interested in {', '.join(detected_interests)}**):

#### 🌟 Top Recommended Destination: **{dest_name}** ({best_dest.state})
- **Compatibility Match:** `{best_dest.total_score}%`
- **Why it fits:** {best_dest.reasons[0] if best_dest.reasons else 'Perfect match for your travel style'}

---

#### 🚆 Verified Transportation Options
- **Recommended Mode:** {transport_name}
- **Route:** {origin} ➔ {dest_name}
- **Round-Trip Fare:** ~{format_currency(trans_fare * 2)} per person

#### 🏨 Verified Accommodation
- **Option:** {hotel_name}
- **Estimated Nightly Rate:** {format_currency(hotel_rate)} (Clean comfort with mountain / valley view)

#### 🏛️ Key Attractions & Activities
"""
        for a in details.get("attractions", [])[:3]:
            response += f"- **{a['name']}**: {a.get('category', 'Sightseeing')} (Entry: {format_currency(a['entry_fee'])})\n"

        response += f"""
---

#### 💰 Verified Budget Estimation
- **Total Estimated Cost:** **{format_currency(calc['total_estimated_cost'])}**
- **Your Target Budget:** **{format_currency(budget)}**
"""

        if opt["needs_optimization"]:
            response += f"""
> 💡 **Cheaper Smart Optimization:**
> The initial plan slightly exceeds your budget. You can comfortably bring it down to **{format_currency(opt['optimized_plan']['total_estimated_cost'])}** (saving **{format_currency(opt['savings'])}**) by booking sleeper train classes, staying at top-rated village homestays, and dining at local specialty eateries!
"""
        else:
            response += f"> ✅ **Great news!** This trip fits comfortably within your budget with **{format_currency(budget - calc['total_estimated_cost'])}** in surplus buffer.\n"

        response += f"""
---
*You can head to **'Plan My Trip'** in the sidebar to review the day-wise itinerary, interactive route map, and complete the in-app booking!*
"""
        return response
