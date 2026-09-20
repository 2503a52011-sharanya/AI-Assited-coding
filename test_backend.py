import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_all():
    print("=== Testing AI Smart Tourism Platform Backend ===")

    # 1. Config
    print("[1/6] Testing Configuration & Settings...")
    from config.settings import settings
    from config.constants import SEED_DESTINATIONS, CURRENCIES
    assert len(SEED_DESTINATIONS) >= 6
    assert "INR" in CURRENCIES
    print("  [OK] Config loaded successfully.")

    # 2. Database & Repositories
    print("[2/6] Testing Database & Repository Layer...")
    from database.connection import db_manager, get_db_collection
    from database.repositories import Repository
    status = db_manager.get_status()
    print(f"  [OK] DB Engine: {status['type']}")

    users = Repository.list_users()
    assert len(users) >= 2, "Seed users should be present"
    print(f"  [OK] Seed users present: {len(users)}")

    destinations = Repository.list_destinations()
    assert len(destinations) >= 6, "Seed destinations should be present"
    print(f"  [OK] Seed destinations present: {len(destinations)}")

    hotels = Repository.list_hotels()
    assert len(hotels) >= 3, "Seed hotels should be present"
    print(f"  [OK] Seed hotels present: {len(hotels)}")

    # 3. Geocoding & Weather Services
    print("[3/6] Testing Geocoding & Weather Services...")
    from services.geocoding_service import geocoding_service
    from services.weather_service import weather_service
    coords = geocoding_service.get_coordinates("Hyderabad")
    assert coords is not None
    print(f"  [OK] Hyderabad Geocoded to: {coords}")

    w = weather_service.get_weather(coords[0], coords[1], "Hyderabad")
    print(f"  [OK] Weather response (Live: {w.get('is_live')}): Temp={w.get('temperature')}, Cond={w.get('condition')}")

    # 4. Recommendation Engine & AI Service
    print("[4/6] Testing Recommendation Engine & AI Fallback...")
    from services.recommendation_engine import recommendation_engine
    from services.ai_service import ai_service
    plan = ai_service.generate_trip_plan(
        start_location="Hyderabad",
        destination="Goa",
        start_date="2026-10-01",
        end_date="2026-10-04",
        days=4,
        travelers=2,
        budget=30000,
        currency="INR",
        travel_style="Standard",
        interests=["Beaches", "Food"],
        accommodation_pref="3 Star",
        food_preferences=["Local Food"],
        transport_preferences=["Train"],
        weather_info=w
    )
    assert "itinerary" in plan
    assert len(plan["itinerary"]) == 4
    assert "estimated_costs" in plan
    print(f"  [OK] Generated 4-day plan. Est cost: INR {plan['estimated_costs']['total_estimated']}")
    print(f"  [OK] AI Notice: {plan.get('ai_notice')}")

    # 5. Export Services (PDF, JSON, CSV)
    print("[5/6] Testing Export Engine...")
    from services.export_service import export_service
    pdf_bytes = export_service.generate_pdf(plan)
    assert len(pdf_bytes) > 500, "PDF generation should output valid bytes"
    csv_str = export_service.generate_csv(plan)
    assert len(csv_str) > 100, "CSV generation should output string"
    json_str = export_service.generate_json(plan)
    assert len(json_str) > 100, "JSON generation should output string"
    print(f"  [OK] PDF generated: {len(pdf_bytes)} bytes | CSV: {len(csv_str)} chars | JSON: {len(json_str)} chars")

    # 6. Streamlit Views Import Check
    print("[6/6] Verifying View Modules Imports...")
    import views.landing
    import views.auth
    import views.traveler_dashboard
    import views.plan_trip
    import views.trip_results
    import views.explore
    import views.hotels_view
    import views.restaurants_view
    import views.transport_view
    import views.weather_view
    import views.budget_view
    import views.favorites_view
    import views.my_trips_view
    import views.ai_assistant_view
    import views.profile_view
    import views.provider_portal
    import views.admin_portal
    print("  [OK] All view modules imported cleanly without errors.")

    print("\nALL BACKEND CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_all()
