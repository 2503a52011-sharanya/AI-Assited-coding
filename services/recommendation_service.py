import logging
from database.queries import get_all_destinations, get_user_preferences, fetch_all
from models.recommendation import RecommendationScore

logger = logging.getLogger(__name__)


class RecommendationService:
    @staticmethod
    def get_personalized_recommendations(
        origin: str,
        user_id: int = None,
        target_budget: float = None,
        days: int = 3,
        traveler_type: str = "All Travelers",
        interests: list = None,
        limit: int = 6
    ) -> list[RecommendationScore]:
        """Calculates multi-criteria recommendation scores across all destinations."""
        destinations = get_all_destinations(limit=100)
        
        # User profile preferences if user_id is provided
        user_pref_interests = []
        user_pref_style = "Comfortable"
        if user_id:
            pref = get_user_preferences(user_id)
            if pref and pref.get("interests"):
                user_pref_interests = [i.strip().lower() for i in pref["interests"].split(",") if i.strip()]
            if pref and pref.get("travel_style"):
                user_pref_style = pref["travel_style"]

        # Combined interests
        active_interests = set([i.lower() for i in (interests or [])] + user_pref_interests)
        
        scores = []
        for d in destinations:
            d_tags = [t.strip().lower() for t in (d.get("tags") or "").split(",") if t.strip()]
            d_budget_daily = float(d.get("avg_daily_budget", 3000.0))
            d_name = d["name"]
            
            # 1. Interest Matching Score (0 - 40 points)
            interest_score = 0.0
            matched_tags = []
            if active_interests:
                for tag in d_tags:
                    if any(ui in tag or tag in ui for ui in active_interests):
                        interest_score += 15.0
                        matched_tags.append(tag.title())
                interest_score = min(40.0, interest_score)
            else:
                interest_score = 25.0 # Baseline if no filter selected

            # 2. Budget Fit Score (0 - 30 points)
            budget_score = 20.0
            if target_budget and target_budget > 0:
                est_total = d_budget_daily * days
                ratio = est_total / target_budget
                if 0.5 <= ratio <= 1.0:
                    budget_score = 30.0 # Perfect fit
                elif ratio < 0.5:
                    budget_score = 25.0 # Very affordable
                elif 1.0 < ratio <= 1.3:
                    budget_score = 15.0 # Slightly over
                else:
                    budget_score = 5.0 # Way over
            
            # 3. Traveler Type Fit (0 - 15 points)
            traveler_score = 10.0
            t_lower = traveler_type.lower().strip()
            if t_lower in ["all", "all travelers", "any"]:
                traveler_score = 15.0
            elif traveler_type in ["Couple", "Romantic"] and any(t in d_tags for t in ["romantic", "nature", "beaches", "mountains", "scenic"]):
                traveler_score = 15.0
            elif traveler_type == "Solo" and any(t in d_tags for t in ["backpacker", "adventure", "culture", "nature", "peaceful"]):
                traveler_score = 15.0
            elif traveler_type in ["Family", "Group"] and any(t in d_tags for t in ["family", "history", "religious", "nature", "heritage"]):
                traveler_score = 15.0
            elif traveler_type == "Friends" and any(t in d_tags for t in ["adventure", "trek", "beaches", "nightlife", "nature", "mountains"]):
                traveler_score = 15.0
            elif traveler_type == "Business" and any(t in d_tags for t in ["metro", "city", "heritage", "culture", "leisure"]):
                traveler_score = 15.0

            # 4. Season & Duration Match (0 - 15 points)
            duration_diff = abs(int(d.get("ideal_duration_days", 3)) - days)
            duration_score = max(5.0, 15.0 - (duration_diff * 4.0))

            total_score = min(100.0, round(interest_score + budget_score + traveler_score + duration_score, 1))

            # Generate helpful reason bullet points
            reasons = []
            if matched_tags:
                reasons.append(f"Matches your passion for: {', '.join(matched_tags[:3])}")
            if budget_score >= 25:
                reasons.append(f"Highly affordable estimated cost for {days} days")
            if traveler_score == 15:
                if t_lower in ["all", "all travelers", "any"]:
                    reasons.append("Versatile destination suitable for all traveler types")
                else:
                    reasons.append(f"Ideal match for {traveler_type} travel vibes")
            if d.get("is_popular"):
                reasons.append("Top-rated traveler favorite in India")

            scores.append(RecommendationScore(
                destination_id=d["id"],
                destination_name=d_name,
                state=d["state"],
                total_score=total_score,
                interest_match_score=interest_score,
                budget_fit_score=budget_score,
                traveler_fit_score=traveler_score,
                reasons=reasons,
                image_url=d.get("image_url") or "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
                tags=d.get("tags", ""),
                avg_daily_budget=d_budget_daily,
                ideal_duration_days=d.get("ideal_duration_days", 3)
            ))

        # Sort by total score descending
        scores.sort(key=lambda x: x.total_score, reverse=True)
        return scores[:limit]
