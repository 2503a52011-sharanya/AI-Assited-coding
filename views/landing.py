import streamlit as st
from config.constants import SEED_DESTINATIONS
from ui.components import render_hero

def render_landing_view():
    """Renders the SaaS landing page."""
    render_hero()

    # Call-to-action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🚀 Plan My Trip", use_container_width=True, type="primary"):
            st.session_state.current_page = "Plan My Trip"
            st.rerun()
    with col2:
        if st.button("🌍 Explore Destinations", use_container_width=True):
            st.session_state.current_page = "Explore"
            st.rerun()
    with col3:
        if not st.session_state.get("logged_in"):
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.current_page = "Auth"
                st.session_state.auth_tab = "Login"
                st.rerun()
        else:
            if st.button("👤 Go to Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
    with col4:
        if not st.session_state.get("logged_in"):
            if st.button("✨ Create Account", use_container_width=True):
                st.session_state.current_page = "Auth"
                st.session_state.auth_tab = "Register"
                st.rerun()
        else:
            if st.button("💬 AI Assistant", use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()

    st.write("")
    st.markdown("### 🌟 Trending Global & Heritage Destinations")
    st.markdown("Discover curated highlights or type **any destination in the world** in our AI Trip Planner.")

    # Show featured destinations grid
    cols = st.columns(3)
    for i, dest in enumerate(SEED_DESTINATIONS[:6]):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="travel-card">
                <img src="{dest['image_url']}" alt="{dest['name']}">
                <div class="travel-card-body">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #2DD4BF; text-transform: uppercase;">
                        {dest['category']} • {dest['country']}
                    </span>
                    <div class="travel-card-title">{dest['name']}</div>
                    <div class="travel-card-subtitle">{dest['description'][:110]}...</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.8rem; border-top: 1px solid #23324F; padding-top: 0.5rem;">
                        <span style="font-size: 0.85rem; color: #94A3B8;">Best Season: <b style="color: #F8FAFC;">{dest['best_season']}</b></span>
                        <span class="travel-card-price">★ {dest['popularity_score']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Plan Trip to {dest['name']}", key=f"btn_land_plan_{dest['id']}", use_container_width=True):
                st.session_state.prefill_destination = dest["name"]
                st.session_state.current_page = "Plan My Trip"
                st.rerun()

    st.write("")
    # Key platform capabilities
    st.markdown("---")
    st.markdown("### ⚡ Why Modern Travelers Choose Our AI Platform")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("""
        #### 🤖 Gemini-Powered Customization
        Dynamic day-by-day itineraries that adapt specifically to your travel mood, party size, and pace.
        """)
    with f_col2:
        st.markdown("""
        #### 💰 Intelligent Budget Optimizer
        Zero guesswork. Compare flights vs. trains, 5-star vs. boutique stays, and receive instant money-saving alternatives.
        """)
    with f_col3:
        st.markdown("""
        #### ☀️ Weather-Aware Scheduling
        Automatic outdoor vs. indoor itinerary adjustment based on live rainfall probabilities and forecast conditions.
        """)
