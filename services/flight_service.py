import logging
import random
from config.settings import FLIGHT_API_KEY, DEMO_MODE_FLIGHTS
from database.queries import fetch_all

logger = logging.getLogger(__name__)


class FlightService:
    @staticmethod
    def search_flights(origin: str, destination: str, travel_date: str, sort_by: str = "Cheapest"):
        """Searches available flights with live API adapter structure or realistic demo catalog."""
        # 1. Query database configured routes first
        db_flights = fetch_all("""
        SELECT * FROM transport_options 
        WHERE transport_type = 'Flight'
          AND (LOWER(origin) LIKE :o OR :o LIKE '%' || LOWER(origin) || '%')
          AND (LOWER(destination) LIKE :d OR :d LIKE '%' || LOWER(destination) || '%')
        """, {"o": f"%{origin.lower()}%", "d": f"%{destination.lower()}%"})

        results = []
        if db_flights:
            for f in db_flights:
                results.append({
                    "id": f["id"],
                    "provider": f["carrier_name"],
                    "flight_number": f.get("service_number", "6E-301"),
                    "departure": f["departure_time"],
                    "arrival": f["arrival_time"],
                    "duration_hours": f["duration_hours"],
                    "duration_str": f"{int(f['duration_hours'])}h {int((f['duration_hours'] % 1) * 60)}m",
                    "price_economy": float(f["fare_economy"]),
                    "price_business": float(f["fare_premium"] or f["fare_economy"] * 2.2),
                    "seats_available": f["available_seats"],
                    "is_demo": True,
                    "cancellation": f.get("cancellation_policy", "Standard airline refund rules")
                })
        else:
            # Dynamic generator for any city pair
            airlines = [("IndiGo", "6E"), ("Air India Express", "IX"), ("Vistara", "UK"), ("Akasa Air", "QP")]
            base_price = 3200.0 + (hash(f"{origin}_{destination}") % 2500)
            
            for idx, (air, code) in enumerate(airlines):
                dur = round(1.5 + (idx * 0.5), 1)
                dep_hour = 6 + (idx * 4)
                arr_hour = (dep_hour + int(dur)) % 24
                price = base_price + (idx * 650)
                results.append({
                    "id": 1000 + idx,
                    "provider": f"{air} Airlines",
                    "flight_number": f"{code}-{random.randint(200, 899)}",
                    "departure": f"{dep_hour:02d}:30",
                    "arrival": f"{arr_hour:02d}:45",
                    "duration_hours": dur,
                    "duration_str": f"{int(dur)}h {int((dur % 1) * 60)}m",
                    "price_economy": price,
                    "price_business": price * 2.1,
                    "seats_available": 12 + (idx * 6),
                    "is_demo": True,
                    "cancellation": "Cancellation fee ₹2500 applies up to 2 hours before flight"
                })

        # Sorting logic
        if sort_by == "Cheapest":
            results.sort(key=lambda x: x["price_economy"])
        elif sort_by == "Fastest":
            results.sort(key=lambda x: x["duration_hours"])
        elif sort_by == "Best Value":
            results.sort(key=lambda x: (x["price_economy"] * 0.6) + (x["duration_hours"] * 300))

        return results
