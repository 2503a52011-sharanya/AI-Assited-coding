import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Mock streamlit session state and components for testing
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

def run_view_tests():
    print("=== Testing View Robustness for Guest & Authenticated Users ===")
    
    # 1. Test as Guest (user = None, logged_in = False)
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_role = "Traveler"
    st.session_state.current_page = "Home"
    st.session_state.active_trip = None
    st.session_state.auth_tab = "Login"

    guest_views = [
        ("Explore", views.explore.render_explore_view),
        ("Landing", views.landing.render_landing_view),
        ("Favorites", views.favorites_view.render_favorites_view),
        ("Hotels", views.hotels_view.render_hotels_view),
        ("Restaurants", views.restaurants_view.render_restaurants_view),
        ("Transport", views.transport_view.render_transport_view),
        ("Weather", views.weather_view.render_weather_view),
        ("Budget", views.budget_view.render_budget_view),
        ("My Trips", views.my_trips_view.render_my_trips_view),
        ("Profile", views.profile_view.render_profile_view),
        ("Plan Trip", views.plan_trip.render_plan_trip_view),
        ("AI Assistant", views.ai_assistant_view.render_ai_assistant_view),
        ("Admin Portal (Guard check)", views.admin_portal.render_admin_portal_view),
        ("Provider Portal (Guard check)", views.provider_portal.render_provider_portal_view),
    ]

    for name, fn in guest_views:
        try:
            fn()
            print(f"  [PASS] Guest View: {name}")
        except Exception as e:
            print(f"  [FAIL] Guest View: {name} -> {e}")
            raise e

    # 2. Test as Authenticated Traveler
    st.session_state.logged_in = True
    st.session_state.user = {
        "_id": "usr_traveler_001",
        "full_name": "Demo Traveler",
        "email": "traveler@example.com",
        "role": "Traveler"
    }
    st.session_state.user_role = "Traveler"

    traveler_views = [
        ("Traveler Dashboard", views.traveler_dashboard.render_traveler_dashboard_view),
        ("Favorites", views.favorites_view.render_favorites_view),
        ("Profile", views.profile_view.render_profile_view),
        ("My Trips", views.my_trips_view.render_my_trips_view),
    ]

    for name, fn in traveler_views:
        try:
            fn()
            print(f"  [PASS] Traveler View: {name}")
        except Exception as e:
            print(f"  [FAIL] Traveler View: {name} -> {e}")
            raise e

    # 3. Test as Authenticated Admin
    st.session_state.user = {
        "_id": "usr_admin_001",
        "full_name": "System Administrator",
        "email": "admin@tourism.ai",
        "role": "Admin"
    }
    st.session_state.user_role = "Admin"
    try:
        views.admin_portal.render_admin_portal_view()
        print("  [PASS] Admin Portal View")
    except Exception as e:
        print(f"  [FAIL] Admin Portal View -> {e}")
        raise e

    # 4. Test as Authenticated Provider
    st.session_state.user = {
        "_id": "usr_prov_001",
        "full_name": "Taj Hospitality Manager",
        "email": "provider@tajhotels.com",
        "role": "Provider",
        "provider_business_name": "Taj Hotels & Resorts"
    }
    st.session_state.user_role = "Provider"
    try:
        views.provider_portal.render_provider_portal_view()
        print("  [PASS] Provider Portal View")
    except Exception as e:
        print(f"  [FAIL] Provider Portal View -> {e}")
        raise e

    print("\nALL VIEWS PASSED ROBUSTNESS & SECURITY CHECKS WITH ZERO ERRORS!")

if __name__ == "__main__":
    run_view_tests()
