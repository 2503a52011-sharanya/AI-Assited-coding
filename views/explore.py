import streamlit as st
from database.repositories import Repository
from ui.components import render_section_header
from services.currency_service import currency_service

def render_explore_view():
    render_section_header("Explore Global Destinations 🌍", "Filter curated tourist magnets or jump into planning your custom dream trip")

    # Search and Category Filters
    c1, c2 = st.columns([1.5, 1])
    with c1:
        search_term = st.text_input("🔍 Search destinations", placeholder="e.g. Goa, Hyderabad, Paris, Kyoto...").strip()
    with c2:
        categories = ["All", "Beach", "Historical", "Culture", "Nature", "Adventure", "Religious", "Food", "Architecture"]
        selected_cat = st.selectbox("Category", categories)

    destinations = Repository.list_destinations(
        category=selected_cat if selected_cat != "All" else None,
        search=search_term if search_term else None
    )

    if not destinations:
        st.info(f"No preset destinations found for '{search_term}'. You can still plan an AI trip to **{search_term}** directly!")
        if st.button(f"🚀 Plan AI Trip to '{search_term}'", type="primary"):
            st.session_state.prefill_destination = search_term
            st.session_state.current_page = "Plan My Trip"
            st.rerun()
        return

    # Render Grid of Destination Cards
    cols = st.columns(3)
    for idx, d in enumerate(destinations):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="travel-card">
                <img src="{d.get('image_url', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80')}" alt="{d.get('name')}">
                <div class="travel-card-body">
                    <span style="font-size: 0.75rem; font-weight: 700; color: #2DD4BF; text-transform: uppercase;">
                        {d.get('category')} • {d.get('country', 'India')}
                    </span>
                    <div class="travel-card-title">{d.get('name')}</div>
                    <div class="travel-card-subtitle">{d.get('description', '')[:120]}...</div>
                    <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 0.5rem;">
                        <b>Top Attractions:</b> {", ".join(d.get('top_attractions', [])[:3])}...
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #23324F; padding-top: 0.6rem;">
                        <span style="font-size: 0.85rem; color: #94A3B8;">Avg: <b style="color: #F8FAFC;">{currency_service.format_currency(d.get('avg_budget_inr', 18000), 'INR')}</b></span>
                        <span class="travel-card-price">★ {d.get('popularity_score', 4.8)}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                if st.button(f"✈️ Plan Trip", key=f"btn_explore_plan_{d.get('_id', d.get('name'))}", use_container_width=True, type="primary"):
                    st.session_state.prefill_destination = d.get("name")
                    st.session_state.current_page = "Plan My Trip"
                    st.rerun()
            with p_col2:
                user = st.session_state.get("user") or {}
                user_id = user.get("_id", "guest_traveler")
                if st.button(f"❤️ Save", key=f"btn_explore_fav_{d.get('_id', d.get('name'))}", use_container_width=True):
                    Repository.toggle_favorite(
                        user_id=user_id,
                        item_id=d.get("_id", d.get("name")),
                        item_type="destination",
                        title=d.get("name"),
                        image_url=d.get("image_url", ""),
                        destination=d.get("name"),
                        price_info=f"Avg {currency_service.format_currency(d.get('avg_budget_inr', 18000), 'INR')}"
                    )
                    st.success("Destination saved to favorites!")
