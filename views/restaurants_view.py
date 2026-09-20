import streamlit as st
from database.repositories import Repository
from ui.components import render_section_header
from services.currency_service import currency_service

def render_restaurants_view():
    render_section_header("Culinary & Dining Guide 🍽️", "Discover celebrated culinary gems, street food trails, and fine dining hotspots")

    # Filters
    c1, c2, c3 = st.columns(3)
    with c1:
        dest_filter = st.text_input("Filter by Destination", placeholder="e.g. Hyderabad, Goa, Delhi...").strip()
    with c2:
        cuisines = ["All", "Hyderabadi / Indian", "Mughlai & Biryani", "Goan & Coastal Seafood", "Parsi & Iranian", "Rajasthani Royal Dining", "Continental"]
        cuisine_choice = st.selectbox("Cuisine", cuisines)
    with c3:
        food_prefs = ["All", "Vegetarian", "Non-Vegetarian", "Local Food", "Fine Dining", "Street Food"]
        food_choice = st.selectbox("Dining Style", food_prefs)

    restaurants = Repository.list_restaurants(
        destination=dest_filter if dest_filter else None,
        cuisine=cuisine_choice if cuisine_choice != "All" else None,
        food_pref=food_choice if food_choice != "All" else None
    )

    if not restaurants:
        st.info("No dining spots matched your criteria.")
        return

    cols = st.columns(3)
    for idx, r in enumerate(restaurants):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="travel-card">
                <img src="{r.get('image_url', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=500&q=80')}" alt="{r.get('name')}">
                <div class="travel-card-body">
                    <span style="font-size: 0.75rem; color: #2DD4BF; font-weight: 700;">{r.get('cuisine')} • {r.get('price_level')}</span>
                    <div class="travel-card-title">{r.get('name')}</div>
                    <div class="travel-card-subtitle">📍 {r.get('address')}</div>
                    <p style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 0.5rem;">{r.get('description')}</p>
                    <div style="font-size: 0.8rem; color: #94A3B8;">🕒 Hours: {r.get('opening_hours', 'Open Daily')}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #23324F; padding-top: 0.6rem; margin-top: 0.6rem;">
                        <span style="font-size: 0.85rem; color: #94A3B8;">Avg Meal: <b style="color: #F8FAFC;">{currency_service.format_currency(r.get('avg_cost_per_person', 650), 'INR')}</b></span>
                        <span class="travel-card-price">★ {r.get('rating', 4.6)}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            user = st.session_state.get("user") or {}
            user_id = user.get("_id", "guest_traveler")
            if st.button(f"❤️ Save {r.get('name')[:14]}", key=f"btn_save_r_{idx}", use_container_width=True):
                Repository.toggle_favorite(
                    user_id=user_id,
                    item_id=r.get("_id", r.get("name")),
                    item_type="restaurant",
                    title=r.get("name"),
                    image_url=r.get("image_url", ""),
                    destination=r.get("destination", ""),
                    price_info=f"Avg {currency_service.format_currency(r.get('avg_cost_per_person', 650), 'INR')}"
                )
                st.success("Saved to favorites!")
