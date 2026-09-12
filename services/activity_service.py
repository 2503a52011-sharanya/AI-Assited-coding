import logging
from database.queries import get_activities_by_destination, get_attractions_by_destination

logger = logging.getLogger(__name__)


class ActivityService:
    @staticmethod
    def get_destination_activities(destination_id: int):
        activities = get_activities_by_destination(destination_id)
        return [{
            "id": a["id"],
            "title": a["title"],
            "category": a["category"],
            "description": a["description"],
            "price_per_person": float(a["price_per_person"]),
            "duration_hours": float(a["duration_hours"]),
            "suitable_for": a.get("suitable_for", "All"),
            "rating": float(a["rating"])
        } for a in activities]

    @staticmethod
    def get_destination_attractions(destination_id: int):
        attractions = get_attractions_by_destination(destination_id)
        return [{
            "id": att["id"],
            "name": att["name"],
            "category": att["category"],
            "description": att["description"],
            "entry_fee": float(att["entry_fee"]),
            "opening_time": att["opening_time"],
            "closing_time": att["closing_time"],
            "duration_hours": float(att["avg_visit_duration_hours"]),
            "is_indoor": bool(att["is_indoor"]),
            "rating": float(att["rating"]),
            "latitude": float(att["latitude"]) if att["latitude"] else None,
            "longitude": float(att["longitude"]) if att["longitude"] else None
        } for att in attractions]
