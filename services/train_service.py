import logging
import random
from database.queries import fetch_all

logger = logging.getLogger(__name__)


class TrainService:
    @staticmethod
    def search_trains(origin: str, destination: str, travel_date: str, sort_by: str = "Cheapest"):
        """Searches trains between origin and destination with IRCTC classes and live/fallback schedule."""
        db_trains = fetch_all("""
        SELECT * FROM transport_options 
        WHERE transport_type = 'Train'
          AND (LOWER(origin) LIKE :o OR :o LIKE '%' || LOWER(origin) || '%')
          AND (LOWER(destination) LIKE :d OR :d LIKE '%' || LOWER(destination) || '%')
        """, {"o": f"%{origin.lower()}%", "d": f"%{destination.lower()}%"})

        results = []
        if db_trains:
            for t in db_trains:
                results.append({
                    "id": t["id"],
                    "train_name": t["carrier_name"],
                    "train_number": t.get("service_number", "17016"),
                    "departure": t["departure_time"],
                    "arrival": t["arrival_time"],
                    "duration_hours": t["duration_hours"],
                    "duration_str": f"{int(t['duration_hours'])}h {int((t['duration_hours'] % 1) * 60)}m",
                    "fare_sleeper": float(t["fare_economy"]),
                    "fare_3ac": float(t["fare_economy"]) * 2.5,
                    "fare_2ac": float(t["fare_premium"] or (float(t["fare_economy"]) * 3.8)),
                    "available_seats": t["available_seats"],
                    "classes": ["SL", "3A", "2A", "1A"],
                    "is_demo": True,
                    "cancellation": t.get("cancellation_policy", "IRCTC standard rules: full refund minus clerkage before 48h")
                })
        else:
            train_names = ["Superfast Express", "Jan Shatabdi Express", "Garib Rath Express", "Intercity Express"]
            base_fare = 280.0 + (hash(f"{origin}_{destination}") % 250)
            base_duration = 5.5 + (hash(f"{destination}") % 8)

            for idx, name in enumerate(train_names):
                dep_hr = 5 + (idx * 5)
                dur = base_duration + (idx * 0.8)
                arr_hr = (dep_hr + int(dur)) % 24
                results.append({
                    "id": 2000 + idx,
                    "train_name": f"{origin} - {destination} {name}",
                    "train_number": f"{12000 + random.randint(100, 999)}",
                    "departure": f"{dep_hr:02d}:15",
                    "arrival": f"{arr_hr:02d}:45",
                    "duration_hours": round(dur, 1),
                    "duration_str": f"{int(dur)}h {int((dur % 1) * 60)}m",
                    "fare_sleeper": round(base_fare + (idx * 40), 0),
                    "fare_3ac": round((base_fare + (idx * 40)) * 2.6, 0),
                    "fare_2ac": round((base_fare + (idx * 40)) * 3.7, 0),
                    "available_seats": 25 + (idx * 12),
                    "classes": ["SL", "3A", "2A"],
                    "is_demo": True,
                    "cancellation": "IRCTC standard refund policy applies"
                })

        if sort_by == "Cheapest":
            results.sort(key=lambda x: x["fare_sleeper"])
        elif sort_by == "Fastest":
            results.sort(key=lambda x: x["duration_hours"])
        elif sort_by == "Best Value":
            results.sort(key=lambda x: (x["fare_3ac"] * 0.7) + (x["duration_hours"] * 80))

        return results
