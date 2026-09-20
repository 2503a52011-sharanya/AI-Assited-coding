from typing import List, Dict, Any, Optional
from database.repositories import Repository
from services.currency_service import currency_service

class TransportService:
    @staticmethod
    def get_transport_options(
        start_location: str,
        destination: str,
        travelers: int = 1,
        currency: str = "INR"
    ) -> List[Dict[str, Any]]:
        # Check DB for pre-recorded routes
        routes = Repository.list_transports(from_loc=start_location, to_loc=destination)
        
        if not routes:
            # Generate realistic multi-modal options
            routes = [
                {
                    "type": "Flight",
                    "from_location": start_location,
                    "to_location": destination,
                    "duration": "1h 45m - 2h 30m",
                    "cost_per_person_inr": 4800,
                    "convenience": "Very High",
                    "vehicle_details": "Commercial Jet (e.g. Indigo / Air India Express / Vistara)",
                    "description": f"Fastest aerial route connecting {start_location} and {destination}.",
                    "availability_note": "Estimated market fares (Demo Mode - live flight API unlinked)"
                },
                {
                    "type": "Train (Express / AC Chair)",
                    "from_location": start_location,
                    "to_location": destination,
                    "duration": "6h 15m - 8h 30m",
                    "cost_per_person_inr": 1250,
                    "convenience": "High",
                    "vehicle_details": "Superfast / Vande Bharat / Express (AC Tier)",
                    "description": f"Comfortable scenic intercity rail passage from {start_location}.",
                    "availability_note": "Standard IRCTC rail estimate"
                },
                {
                    "type": "Private AC Cab / Rental Car",
                    "from_location": start_location,
                    "to_location": destination,
                    "duration": "7h 00m - 9h 30m",
                    "cost_per_person_inr": int(6500 / max(1, travelers)),
                    "total_vehicle_cost_inr": 6500,
                    "convenience": "Maximum Flexibility",
                    "vehicle_details": "Sedan / SUV with dedicated chauffeur",
                    "description": "Door-to-door flexibility with highway rest stops at your leisure.",
                    "availability_note": "Fleet partner baseline estimate"
                },
                {
                    "type": "Intercity AC Volvo Bus",
                    "from_location": start_location,
                    "to_location": destination,
                    "duration": "8h 30m - 10h 00m",
                    "cost_per_person_inr": 850,
                    "convenience": "Moderate",
                    "vehicle_details": "Multi-axle Sleeper / Semi-sleeper AC Bus",
                    "description": "Budget-friendly overnight transit option.",
                    "availability_note": "Aggregate intercity coach estimate"
                }
            ]

        # Calculate converted costs for group
        result = []
        for r in routes:
            item = dict(r)
            cost_per_person = float(item.get("cost_per_person_inr", item.get("cost", 2000)))
            total_group_cost = cost_per_person * travelers
            item["cost_per_person_converted"] = currency_service.convert(cost_per_person, "INR", currency)
            item["total_cost_converted"] = currency_service.convert(total_group_cost, "INR", currency)
            item["currency"] = currency
            item["travelers"] = travelers
            result.append(item)

        return result

    @staticmethod
    def get_local_transit_options(destination: str, currency: str = "INR") -> List[Dict[str, Any]]:
        """Options for getting around within the destination."""
        options = [
            {
                "mode": "Metro / Light Rail & Public Transit",
                "daily_cost_inr": 150,
                "best_for": "Beating city traffic & budget convenience",
                "coverage": "High in metropolitan centers"
            },
            {
                "mode": "Ride-Hailing & Taxis (Ola / Uber / Local Taxi)",
                "daily_cost_inr": 800,
                "best_for": "Point-to-point comfort with luggage",
                "coverage": "Available across all central tourist hubs"
            },
            {
                "mode": "Auto Rickshaw / Tuk-Tuk",
                "daily_cost_inr": 400,
                "best_for": "Quick short hops and authentic cultural experience",
                "coverage": "Ubiquitous street availability"
            },
            {
                "mode": "Scooter / Self-Drive Bike Rental",
                "daily_cost_inr": 500,
                "best_for": "Couples and solo backpackers exploring coastlines or hill stations",
                "coverage": "Popular in Goa, Kerala, and Rajasthan"
            }
        ]
        for opt in options:
            opt["daily_cost_converted"] = currency_service.convert(opt["daily_cost_inr"], "INR", currency)
            opt["currency"] = currency
        return options

transport_service = TransportService()
