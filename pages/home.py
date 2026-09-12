import streamlit as st
from services.destination_service import DestinationService
from services.recommendation_service import RecommendationService
from utils.helpers import format_currency


def render_home_page():
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 35px 25px; border-radius: 16px; color: white; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0; font-size: 2.3rem;">✈️ AI Smart Tourism & Travel Recommendation System</h1>
        <p style="color: #e0e6ed; font-size: 1.15rem; margin-top: 8px;">
            Your unified single-window travel assistant. Discover remote villages, plan personalized itineraries, optimize budgets, and book trips in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Smart Search Bar (Supports any town, village, or city)
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        search_query = st.text_input(
            "🔍 Where do you want to go?",
            placeholder="Search any destination: e.g. Araku Valley, Hyderabad, Warangal, Ooty, Hampi, Ziro...",
            key="home_search_input",
            label_visibility="collapsed"
        )
    with col_btn:
        search_clicked = st.button("Explore Now", width="stretch", type="primary")

    if search_clicked or (search_query and st.session_state.get("last_searched") != search_query):
        st.session_state["last_searched"] = search_query
        results = DestinationService.search(search_query)
        st.subheader(f"Search Results for '{search_query}'")
        if results:
            for r in results:
                with st.expander(f"📍 {r['name']} ({r.get('state', 'India')})", expanded=True):
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        st.image(r.get("image_url") or "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800", width="stretch")
                    with col_info:
                        st.markdown(f"**Best Season:** {r.get('best_season', 'All year')} | **Ideal Duration:** {r.get('ideal_duration_days', 3)} Days")
                        st.markdown(f"**Estimated Daily Cost:** {format_currency(r.get('avg_daily_budget', 3000.0))}")
                        st.write(r.get("description", ""))
                        if st.button(f"Plan Trip to {r['name']}", key=f"plan_{r['name']}"):
                            st.session_state["selected_destination_name"] = r["name"]
                            target_tt = st.session_state.get("selected_traveler_type", "Solo")
                            if target_tt == "All Travelers":
                                target_tt = "Solo"
                            st.session_state["plan_traveler_type"] = target_tt
                            st.session_state["plan_travelers"] = 1 if target_tt == "Solo" else (2 if target_tt == "Couple" else 4)
                            st.session_state.pop("plan_generated", None)
                            st.switch_page("pages/planner.py")
        else:
            st.info("No exact match found, but our discovery engine can auto-generate details when you enter it in Plan My Trip!")

    st.markdown("---")

    # Quick Navigation Cards
    st.subheader("⚡ Quick Travel Tools")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    with qcol1:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 1.2rem;">🗺️ Plan My Trip</h3>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 6px;">Personalized multi-day planner with auto-budgeting.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Planning", key="btn_quick_plan", width="stretch"):
            target_tt = st.session_state.get("selected_traveler_type", "Solo")
            if target_tt == "All Travelers":
                target_tt = "Solo"
            st.session_state["plan_traveler_type"] = target_tt
            st.session_state["plan_travelers"] = 1 if target_tt == "Solo" else (2 if target_tt == "Couple" else 4)
            st.session_state.pop("plan_generated", None)
            st.switch_page("pages/planner.py")

    with qcol2:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 1.2rem;">💰 Budget Optimizer</h3>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 6px;">Compare original vs smart optimized trip costs.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Optimize Budget", key="btn_quick_budget", width="stretch"):
            st.switch_page("pages/budget.py")

    with qcol3:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 1.2rem;">🚆 Transportation</h3>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 6px;">Search and book Flights, Trains, Buses, & Cabs.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Search Transport", key="btn_quick_trans", width="stretch"):
            st.switch_page("pages/transportation.py")

    with qcol4:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 1.2rem;">🏨 Hotels & Stays</h3>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 6px;">Find verified homestays, resorts, & budget stays.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Find Stays", key="btn_quick_hotels", width="stretch"):
            st.switch_page("pages/hotels.py")

    st.markdown("---")

    # Personalized AI Recommendations Grid
    st.subheader("🌟 Top Recommended Destinations for You")
    st.caption("Dynamically scored based on your travel group, trending popularity, season, and regional charm.")
    
    col_t1, col_t2 = st.columns([2, 3])
    with col_t1:
        traveler_options = ["All Travelers", "Solo", "Couple", "Family", "Friends", "Group", "Business"]
        default_tt = st.session_state.get("selected_traveler_type", "All Travelers")
        default_idx = traveler_options.index(default_tt) if default_tt in traveler_options else 0
        selected_traveler_type = st.selectbox("Traveler Type Preference", traveler_options, index=default_idx, key="home_traveler_type_sel")
        st.session_state["selected_traveler_type"] = selected_traveler_type
    with col_t2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption(f"Showing tailored recommendations optimized for: **{selected_traveler_type}**")

    recs = RecommendationService.get_personalized_recommendations(
        origin="Hyderabad",
        user_id=st.session_state.get("user_id"),
        target_budget=20000.0,
        days=3,
        traveler_type=selected_traveler_type,
        limit=6
    )

    r_cols = st.columns(3)
    for idx, rec in enumerate(recs):
        with r_cols[idx % 3]:
            st.image(rec.image_url, width="stretch")
            st.markdown(f"### {rec.destination_name}")
            st.markdown(f"**State:** {rec.state} | **Match Score:** `{rec.total_score}%`")
            st.markdown(f"**Avg Daily:** {format_currency(rec.avg_daily_budget)}")
            if rec.reasons:
                st.caption(f"✨ {rec.reasons[0]}")
            
            c_det, c_plan = st.columns(2)
            with c_det:
                if st.button("View", key=f"rec_view_{rec.destination_id}", width="stretch"):
                    st.session_state["selected_dest_id"] = rec.destination_id
                    st.switch_page("pages/destinations.py")
            with c_plan:
                if st.button("Plan", key=f"rec_plan_{rec.destination_id}", type="primary", width="stretch"):
                    st.session_state["selected_destination_name"] = rec.destination_name
                    target_tt = selected_traveler_type if selected_traveler_type != "All Travelers" else "Solo"
                    st.session_state["selected_traveler_type"] = target_tt
                    st.session_state["plan_traveler_type"] = target_tt
                    st.session_state["plan_travelers"] = 1 if target_tt == "Solo" else (2 if target_tt == "Couple" else 4)
                    st.session_state.pop("plan_generated", None)
                    st.switch_page("pages/planner.py")


render_home_page()

