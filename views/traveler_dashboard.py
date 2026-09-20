import streamlit as st
from database.repositories import Repository
from ui.components import render_kpi_card, render_section_header
from config.constants import SEED_DESTINATIONS
from services.currency_service import currency_service

def render_traveler_dashboard_view():
    user = st.session_state.get("user") or {}
    user_id = user.get("_id", "guest")
    user_name = user.get("full_name", "Traveler")

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 class="page-title">Good morning, {user_name} 👋</h1>
        <p class="page-subtitle">Here is your travel command center, live itineraries, and destination intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch User Stats
    kpis = Repository.get_traveler_kpis(user_id)
    trips = Repository.get_user_trips(user_id)
    favorites = Repository.get_user_favorites(user_id)
    bookings = Repository.get_user_bookings(user_id)

    # KPI Cards Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Trips Planned", str(kpis["trips_planned"]), "Total custom plans")
    with c2:
        render_kpi_card("Favorite Places", str(kpis["favorites_count"]), "Saved stays & spots")
    with c3:
        render_kpi_card("Upcoming Trip", kpis["upcoming_trip"], "Next scheduled getaway")
    with c4:
        render_kpi_card("Active Bookings", str(kpis["total_bookings"]), "Confirmed & pending")

    st.write("")
    # Main Dashboard Columns
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        render_section_header("🛫 Your Latest Itineraries", "Pick up right where you left off or plan a new adventure")
        if trips:
            latest_trip = trips[0]
            curr = latest_trip.get("currency", "INR")
            cost = latest_trip.get("estimated_costs", {}).get("total_estimated", 0)
            
            st.markdown(f"""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: #0D9488; color: white; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">
                        {latest_trip.get('status', 'Upcoming')}
                    </span>
                    <span style="font-size: 0.85rem; color: #94A3B8;">Created: {latest_trip.get('created_at', '')[:10]}</span>
                </div>
                <h3 style="color: #38BDF8; margin-top: 0.6rem; margin-bottom: 0.3rem;">{latest_trip.get('destination')} Expedition</h3>
                <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0.75rem;">
                    <b>From:</b> {latest_trip.get('start_location')} &nbsp;|&nbsp; 
                    <b>Duration:</b> {latest_trip.get('days')} Days &nbsp;|&nbsp; 
                    <b>Travelers:</b> {latest_trip.get('travelers')}
                </p>
                <div style="font-size: 1.1rem; color: #F8FAFC; margin-bottom: 1rem;">
                    <b>Estimated Total:</b> <span style="color: #FB923C; font-weight: 800;">{currency_service.format_currency(cost, curr)}</span>
                    <span style="font-size: 0.85rem; color: #94A3B8;">(Budget: {currency_service.format_currency(latest_trip.get('budget', 0), curr)})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_view, btn_new = st.columns(2)
            with btn_view:
                if st.button("🔎 View Full Trip Results", use_container_width=True, type="primary"):
                    st.session_state.active_trip = latest_trip
                    st.session_state.current_page = "Trip Results"
                    st.rerun()
            with btn_new:
                if st.button("➕ Generate New AI Trip", use_container_width=True):
                    st.session_state.current_page = "Plan My Trip"
                    st.rerun()
        else:
            st.info("You haven't generated any trips yet! Use our 9-step planner to create your first itinerary.")
            if st.button("🚀 Plan My First Trip", type="primary", use_container_width=True):
                st.session_state.current_page = "Plan My Trip"
                st.rerun()

        st.write("")
        render_section_header("❤️ Saved Favorites & Stays", "Quick access to your bookmarked places")
        if favorites:
            f_cols = st.columns(2)
            for i, fav in enumerate(favorites[:4]):
                with f_cols[i % 2]:
                    st.markdown(f"""
                    <div style="border: 1px solid #334155; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; background: #1E293B;">
                        <span style="font-size: 0.75rem; color: #2DD4BF; font-weight: 700; text-transform: uppercase;">{fav.get('item_type')}</span>
                        <div style="font-weight: 700; color: #F8FAFC; font-size: 1.05rem;">{fav.get('title')}</div>
                        <div style="color: #94A3B8; font-size: 0.85rem;">{fav.get('destination')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("No favorites saved yet. Browse hotels and attractions to bookmark them.")

    with col_right:
        # Quick Actions Card
        st.markdown("""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 16px; padding: 1.25rem; margin-bottom: 1.5rem;">
            <h4 style="color: #38BDF8; margin-bottom: 1rem;">⚡ Quick Tools</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗺️ Explore Destinations Directory", use_container_width=True):
            st.session_state.current_page = "Explore"
            st.rerun()
        if st.button("🏨 Discover Certified Hotels", use_container_width=True):
            st.session_state.current_page = "Hotels"
            st.rerun()
        if st.button("🍽️ Browse Regional Dining", use_container_width=True):
            st.session_state.current_page = "Restaurants"
            st.rerun()
        if st.button("🤖 Ask AI Travel Assistant", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()

        # Recommended Destinations Widget
        st.write("")
        st.markdown("#### 🌟 Top Recommended Spots")
        for d in SEED_DESTINATIONS[:3]:
            st.markdown(f"""
            <div style="display: flex; gap: 12px; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                <img src="{d['image_url']}" style="width: 60px; height: 60px; border-radius: 10px; object-fit: cover;">
                <div>
                    <div style="font-weight: 700; color: #F8FAFC; font-size: 0.95rem;">{d['name']}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8;">{d['category']} • Best in {d['best_season']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
