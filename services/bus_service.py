import logging
import random
from database.queries import fetch_all

logger = logging.getLogger(__name__)


class BusService:
    @staticmethod
    def search_buses(origin: str, destination: str, travel_date: str, sort_by: str = "Cheapest"):
        """Searches buses between cities with bus type (AC Sleeper, Semi-Sleeper, Express)."""
        db_buses = fetch_all("""
        SELECT * FROM transport_options 
        WHERE transport_type = 'Bus'
          AND (LOWER(origin) LIKE :o OR :o LIKE '%' || LOWER(origin) || '%')
          AND (LOWER(destination) LIKE :d OR :d LIKE '%' || LOWER(destination) || '%')
        """, {"o": f"%{origin.lower()}%", "d": f"%{destination.lower()}%"})

        results = []
        if db_buses:
            for b in db_buses:
                results.append({
                    "id": b["id"],
                    "operator": b["carrier_name"],
                    "bus_type": "Multi-Axle AC Sleeper / Semi-Sleeper",
                    "departure": b["departure_time"],
                    "arrival": b["arrival_time"],
                    "duration_hours": b["duration_hours"],
                    "duration_str": f"{int(b['duration_hours'])}h {int((b['duration_hours'] % 1) * 60)}m",
                    "fare": float(b["fare_economy"]),
                    "fare_premium": float(b["fare_premium"] or b["fare_economy"] * 1.3),
                    "available_seats": b["available_seats"],
                    "is_demo": True,
                    "cancellation": b.get("cancellation_policy", "Free cancellation up to 6 hours before departure")
                })
        else:
            operators = [("State Transport RTC", "Super Luxury AC"), ("Orange Travels", "BharatBenz AC Sleeper"),
                         ("Morning Star Travels", "Volvo Multi-Axle"), ("IntrCity SmartBus", "AC Lounge Sleeper")]
            base_fare = 550.0 + (hash(f"{origin}_{destination}") % 400)
            base_duration = 6.0 + (hash(f"{destination}") % 6)

            for idx, (op, btype) in enumerate(operators):
                dep_hr = 19 + idx if (19 + idx) < 24 else (idx)
                dur = base_duration + (idx * 0.5)
                arr_hr = (dep_hr + int(dur)) % 24
                fare = round(base_fare + (idx * 150), 0)
                results.append({
                    "id": 3000 + idx,
                    "operator": op,
                    "bus_type": btype,
                    "departure": f"{dep_hr:02d}:30",
                    "arrival": f"{arr_hr:02d}:00",
                    "duration_hours": round(dur, 1),
                    "duration_str": f"{int(dur)}h {int((dur % 1) * 60)}m",
                    "fare": fare,
                    "fare_premium": fare + 300,
                    "available_seats": 14 + (idx * 5),
                    "is_demo": True,
                    "cancellation": "Free cancellation up to 12 hours before departure"
                })

        if sort_by == "Cheapest":
            results.sort(key=lambda x: x["fare"])
        elif sort_by == "Fastest":
            results.sort(key=lambda x: x["duration_hours"])
        elif sort_by == "Best Value":
            results.sort(key=lambda x: (x["fare"] * 0.7) + (x["duration_hours"] * 100))

        return results
