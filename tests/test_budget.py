import pytest
from services.budget_service import BudgetService


def test_budget_calculation():
    # 3 days, 2 travelers, ₹500 train fare per person, ₹1500 hotel
    calc = BudgetService.calculate_trip_budget(
        days=3,
        travelers=2,
        transport_fare_per_person=500.0,
        hotel_nightly_rate=1500.0,
        food_style="Vegetarian",
        travel_style="Comfortable",
        activities_cost_per_person=200.0,
        local_cab_daily_rate=1000.0
    )

    # Transport: 500 * 2 (round-trip) * 2 = 2000
    assert calc["transport_cost"] == 2000.0
    # Hotel: 1500 * 2 nights * 1 room = 3000
    assert calc["accommodation_cost"] == 3000.0
    # Total estimated should include subtotal + buffer
    assert calc["total_estimated_cost"] > (calc["transport_cost"] + calc["accommodation_cost"])
    assert calc["cost_per_person"] == round(calc["total_estimated_cost"] / 2, 2)


def test_budget_optimization():
    calc = BudgetService.calculate_trip_budget(
        days=3,
        travelers=2,
        transport_fare_per_person=3500.0, # expensive flight
        hotel_nightly_rate=4500.0,         # luxury stay
        food_style="Premium restaurants",
        travel_style="Luxury",
        activities_cost_per_person=1000.0,
        local_cab_daily_rate=2000.0
    )

    # User only has ₹20,000 budget
    user_budget = 20000.0
    assert calc["total_estimated_cost"] > user_budget

    opt = BudgetService.optimize_budget(
        user_budget=user_budget,
        original_plan=calc,
        days=3,
        travelers=2,
        current_transport_type="Flight",
        current_hotel_price=4500.0
    )

    assert opt["needs_optimization"] is True
    assert opt["optimized_plan"]["total_estimated_cost"] < calc["total_estimated_cost"]
    assert opt["savings"] > 0
    assert len(opt["recommendations"]) > 0
