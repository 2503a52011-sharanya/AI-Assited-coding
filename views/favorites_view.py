import streamlit as st
from database.repositories import Repository
from ui.components import render_section_header

def render_favorites_view():
    render_section_header("My Saved Favorites ❤️", "Access your bookmarked hotels, dining spots, attractions, and destinations")

    user = st.session_state.get("user") or {}
    user_id = user.get("_id", "guest_traveler")

    # Filter by type
    type_filter = st.selectbox("Filter by Category", ["All", "hotel", "restaurant", "destination", "activity"])
    favorites = Repository.get_user_favorites(user_id, item_type=type_filter if type_filter != "All" else None)

    if not favorites:
        st.info("You haven't bookmarked any items yet. Browse destinations, hotels, or restaurants and click 'Save'.")
        return

    cols = st.columns(3)
    for idx, fav in enumerate(favorites):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="travel-card">
                <img src="{fav.get('image_url', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=500&q=80')}">
                <div class="travel-card-body">
                    <span style="font-size: 0.75rem; color: #2DD4BF; font-weight: 700; text-transform: uppercase;">{fav.get('item_type')}</span>
                    <div class="travel-card-title">{fav.get('title')}</div>
                    <div class="travel-card-subtitle">📍 {fav.get('destination', 'Location')}</div>
                    <div style="font-size: 0.85rem; color: #FB923C; font-weight: 700; margin-bottom: 0.5rem;">{fav.get('price_info', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            b1, b2 = st.columns(2)
            with b1:
                if fav.get("item_type") == "destination":
                    if st.button("✈️ Plan Trip", key=f"fav_plan_{fav.get('_id')}", use_container_width=True):
                        st.session_state.prefill_destination = fav.get("title")
                        st.session_state.current_page = "Plan My Trip"
                        st.rerun()
                else:
                    st.write("")
            with b2:
                if st.button("🗑️ Remove", key=f"fav_del_{fav.get('_id')}", use_container_width=True):
                    Repository.toggle_favorite(user_id, fav.get("item_id"), fav.get("item_type"), fav.get("title"))
                    st.success("Removed!")
                    st.rerun()
