import streamlit as st
from config.settings import settings
from ui.styles import get_custom_css
from database.repositories import Repository

# Page configuration MUST be first Streamlit command
st.set_page_config(
    page_title="AI Smart Tourism & Travel Recommendation Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize global session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_role = "Traveler"  # Default role
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "active_trip" not in st.session_state:
    st.session_state.active_trip = None
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "Login"

# Import view components
from views.landing import render_landing_view
from views.auth import render_auth_view
from views.traveler_dashboard import render_traveler_dashboard_view
from views.plan_trip import render_plan_trip_view
from views.trip_results import render_trip_results_view
from views.explore import render_explore_view
from views.hotels_view import render_hotels_view
from views.restaurants_view import render_restaurants_view
from views.transport_view import render_transport_view
from views.weather_view import render_weather_view
from views.budget_view import render_budget_view
from views.favorites_view import render_favorites_view
from views.my_trips_view import render_my_trips_view
from views.ai_assistant_view import render_ai_assistant_view
from views.profile_view import render_profile_view
from views.provider_portal import render_provider_portal_view
from views.admin_portal import render_admin_portal_view

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0; text-align: left; margin-bottom: 1rem;">
        <span style="font-size: 1.4rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
            ✈️ TOURISM.<span style="color: #F97316;">AI</span>
        </span>
        <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.2rem;">Smart Travel Recommendation Platform</div>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")
    user_role = st.session_state.get("user_role", "Traveler")

    if st.session_state.logged_in and user:
        role_badge = "#0D9488" if user_role == "Traveler" else ("#7C3AED" if user_role == "Provider" else "#DC2626")
        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 10px; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #334155;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #FFFFFF;">{user.get('full_name')}</div>
            <span style="background: {role_badge}; color: white; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">
                {user_role}
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Dynamic Navigation depending on Role
    nav_options = []
    if not st.session_state.logged_in:
        nav_options = [
            "Home",
            "Plan My Trip",
            "Explore",
            "Hotels",
            "Restaurants",
            "Transport",
            "Weather",
            "AI Assistant",
            "Sign In / Register"
        ]
    elif user_role == "Traveler":
        nav_options = [
            "Dashboard",
            "Plan My Trip",
            "Explore",
            "Hotels",
            "Restaurants",
            "Transport",
            "Weather",
            "Budget",
            "Favorites",
            "My Trips",
            "AI Assistant",
            "Profile"
        ]
        if st.session_state.active_trip:
            nav_options.insert(2, "Trip Results")

    elif user_role == "Provider":
        nav_options = [
            "Provider Portal",
            "Explore",
            "Profile"
        ]

    elif user_role == "Admin":
        nav_options = [
            "Admin Portal",
            "Explore",
            "Profile"
        ]

    # Map current_page to selectbox index
    current_page = st.session_state.current_page
    if current_page == "Landing":
        current_page = "Home"
    if current_page == "Auth":
        current_page = "Sign In / Register"

    page_index = 0
    if current_page in nav_options:
        page_index = nav_options.index(current_page)

    selected_nav = st.radio("Navigation", nav_options, index=page_index, label_visibility="collapsed")

    # Sync selection
    target_page = selected_nav
    if target_page == "Home":
        target_page = "Landing"
    elif target_page == "Sign In / Register":
        target_page = "Auth"

    if target_page != st.session_state.current_page:
        st.session_state.current_page = target_page
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.72rem; color: #64748B; text-align: center;">
        v1.0.0 • Resilient Engine<br>
        Powered by Google Gemini & MongoDB
    </div>
    """, unsafe_allow_html=True)


# --- ROUTER DISPATCH ---
current = st.session_state.current_page

if current == "Landing" or current == "Home":
    render_landing_view()
elif current == "Auth":
    render_auth_view()
elif current == "Dashboard":
    render_traveler_dashboard_view()
elif current == "Plan My Trip":
    render_plan_trip_view()
elif current == "Trip Results":
    render_trip_results_view()
elif current == "Explore":
    render_explore_view()
elif current == "Hotels":
    render_hotels_view()
elif current == "Restaurants":
    render_restaurants_view()
elif current == "Transport":
    render_transport_view()
elif current == "Weather":
    render_weather_view()
elif current == "Budget":
    render_budget_view()
elif current == "Favorites":
    render_favorites_view()
elif current == "My Trips":
    render_my_trips_view()
elif current == "AI Assistant":
    render_ai_assistant_view()
elif current == "Profile":
    render_profile_view()
elif current == "Provider Portal":
    render_provider_portal_view()
elif current == "Admin Portal":
    render_admin_portal_view()
else:
    render_landing_view()
