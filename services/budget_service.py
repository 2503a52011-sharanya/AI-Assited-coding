import logging

logger = logging.getLogger(__name__)


class BudgetService:
    @staticmethod
    def calculate_trip_budget(
        days: int,
        travelers: int,
        transport_fare_per_person: float,
        hotel_nightly_rate: float,
        food_style: str = "Local food",
        travel_style: str = "Comfortable",
        activities_cost_per_person: float = 0.0,
        local_cab_daily_rate: float = 1200.0
    ) -> dict:
        """Calculates itemized travel costs including transport, lodging, meals, transit, and emergency buffer."""
        # 1. Total long-distance transport (Round trip)
        transport_cost = transport_fare_per_person * 2 * travelers

        # 2. Accommodation cost (assume 2 adults per room)
        rooms_needed = max(1, (travelers + 1) // 2)
        nights = max(1, days - 1)
        accommodation_cost = hotel_nightly_rate * nights * rooms_needed

        # 3. Daily food cost per person based on food preference
        daily_food_rates = {
            "Budget food": 350.0,
            "Local food": 550.0,
            "Vegetarian": 450.0,
            "Non-vegetarian": 650.0,
            "Vegan": 500.0,
            "Premium restaurants": 1400.0
        }
        daily_food = daily_food_rates.get(food_style, 550.0)
        food_cost = daily_food * days * travelers

        # 4. Activities & sightseeing entrance fees
        activities_cost = activities_cost_per_person * travelers

        # 5. Local internal transportation (auto / local cabs)
        # Scale with group size
        local_transport_cost = local_cab_daily_rate * days * (1.0 if travelers <= 4 else 1.5)

        # 6. Base total
        subtotal = transport_cost + accommodation_cost + food_cost + activities_cost + local_transport_cost

        # 7. Emergency buffer (7% buffer)
        emergency_buffer = round(subtotal * 0.07, 2)
        total_estimated = round(subtotal + emergency_buffer, 2)

        cost_per_person = round(total_estimated / travelers, 2)
        daily_average = round(total_estimated / days, 2)

        # Percentages
        t_pct = round((transport_cost / total_estimated) * 100, 1) if total_estimated > 0 else 0
        h_pct = round((accommodation_cost / total_estimated) * 100, 1) if total_estimated > 0 else 0
        f_pct = round((food_cost / total_estimated) * 100, 1) if total_estimated > 0 else 0
        a_pct = round((activities_cost / total_estimated) * 100, 1) if total_estimated > 0 else 0
        lt_pct = round((local_transport_cost / total_estimated) * 100, 1) if total_estimated > 0 else 0
        b_pct = round((emergency_buffer / total_estimated) * 100, 1) if total_estimated > 0 else 0

        return {
            "transport_cost": round(transport_cost, 2),
            "accommodation_cost": round(accommodation_cost, 2),
            "food_cost": round(food_cost, 2),
            "activities_cost": round(activities_cost, 2),
            "local_transport_cost": round(local_transport_cost, 2),
            "buffer_cost": emergency_buffer,
            "total_estimated_cost": total_estimated,
            "cost_per_person": cost_per_person,
            "daily_average": daily_average,
            "breakdown_percentages": {
                "Transportation": t_pct,
                "Accommodation": h_pct,
                "Food & Dining": f_pct,
                "Activities & Entry": a_pct,
                "Local Transit": lt_pct,
                "Emergency Buffer": b_pct
            }
        }

    @staticmethod
    def optimize_budget(
        user_budget: float,
        original_plan: dict,
        days: int,
        travelers: int,
        current_transport_type: str,
        current_hotel_price: float
    ) -> dict:
        """
        If original plan exceeds user budget, automatically produces an optimized lower-cost alternative
        by switching to smarter transport, value-for-money homestays, free viewpoints, and local dining.
        """
        original_total = original_plan["total_estimated_cost"]
        if original_total <= user_budget:
            return {
                "needs_optimization": False,
                "original_plan": original_plan,
                "optimized_plan": original_plan,
                "savings": 0.0,
                "recommendations": ["Your selected preferences already fit comfortably within your target budget!"]
            }

        # Optimization steps
        recommendations = []
        
        # 1. Transport Optimization
        opt_transport = original_plan["transport_cost"]
        if current_transport_type in ["Flight", "Cab"] and original_total > user_budget:
            # Switch to Sleeper / 3AC train or AC Volvo bus (saves ~50-65%)
            opt_transport = round(original_plan["transport_cost"] * 0.45, 2)
            recommendations.append("Switched long-distance travel to Superfast Express Train / AC Bus.")
        elif opt_transport > (user_budget * 0.4):
            opt_transport = round(opt_transport * 0.7, 2)
            recommendations.append("Optimized travel route booking with advance saver fare.")

        # 2. Hotel Optimization
        opt_accommodation = original_plan["accommodation_cost"]
        if current_hotel_price > 2500.0:
            # Switch to high-rated cozy homestay or boutique budget inn (~₹1,200 - ₹1,500/night)
            nights = max(1, days - 1)
            rooms = max(1, (travelers + 1) // 2)
            opt_accommodation = 1350.0 * nights * rooms
            recommendations.append("Switched lodging to top-rated scenic local Homestay / Heritage Guest House.")
        elif opt_accommodation > (user_budget * 0.35):
            opt_accommodation = round(opt_accommodation * 0.75, 2)
            recommendations.append("Selected economy comfort room tier with complimentary breakfast.")

        # 3. Dining Optimization
        opt_food = round(original_plan["food_cost"] * 0.8, 2)
        recommendations.append("Replaced fine dining with authentic local specialty eateries & thalis.")

        # 4. Activities Optimization
        opt_activities = round(original_plan["activities_cost"] * 0.5, 2)
        recommendations.append("Prioritized free scenic viewpoints, heritage trails, and botanical gardens over expensive commercial tours.")

        # 5. Local transit
        opt_local_transport = round(original_plan["local_transport_cost"] * 0.7, 2)
        recommendations.append("Utilized shared sightseeing jeeps / local day auto-rickshaws for short transit.")

        # New total
        opt_subtotal = opt_transport + opt_accommodation + opt_food + opt_activities + opt_local_transport
        opt_buffer = round(opt_subtotal * 0.05, 2) # 5% buffer
        opt_total = round(opt_subtotal + opt_buffer, 2)
        savings = round(original_total - opt_total, 2)

        optimized_plan = {
            "transport_cost": opt_transport,
            "accommodation_cost": opt_accommodation,
            "food_cost": opt_food,
            "activities_cost": opt_activities,
            "local_transport_cost": opt_local_transport,
            "buffer_cost": opt_buffer,
            "total_estimated_cost": opt_total,
            "cost_per_person": round(opt_total / travelers, 2),
            "daily_average": round(opt_total / days, 2),
            "breakdown_percentages": {
                "Transportation": round((opt_transport / opt_total) * 100, 1),
                "Accommodation": round((opt_accommodation / opt_total) * 100, 1),
                "Food & Dining": round((opt_food / opt_total) * 100, 1),
                "Activities & Entry": round((opt_activities / opt_total) * 100, 1),
                "Local Transit": round((opt_local_transport / opt_total) * 100, 1),
                "Emergency Buffer": round((opt_buffer / opt_total) * 100, 1)
            }
        }

        return {
            "needs_optimization": True,
            "original_plan": original_plan,
            "optimized_plan": optimized_plan,
            "savings": savings,
            "recommendations": recommendations
        }
