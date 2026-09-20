import streamlit as st
from database.repositories import Repository
from database.models import create_booking_doc
from ui.components import render_section_header
from services.currency_service import currency_service

def render_hotels_view():
    render_section_header("Hotels & Stays Directory 🏨", "Browse certified accommodations, check estimated night rates, and request provider reservations")

    # Filters
    f1, f2, f3 = st.columns(3)
    with f1:
        destination_filter = st.text_input("Filter by Destination", placeholder="e.g. Hyderabad, Goa, Delhi...").strip()
    with f2:
        min_stars = st.selectbox("Minimum Star Rating", [0, 3, 4, 5], format_func=lambda x: "All Ratings" if x == 0 else f"{x} Stars & Up")
    with f3:
        max_price = st.number_input("Max Nightly Budget (₹ INR)", min_value=0, value=50000, step=2000)

    hotels = Repository.list_hotels(
        destination=destination_filter if destination_filter else None,
        min_stars=min_stars if min_stars > 0 else None,
        max_price=max_price if max_price > 0 else None
    )

    st.markdown("""
    <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1rem;">
        ℹ️ <i>Notice: Room rates shown are provider-estimated baselines. Real-time availability is confirmed upon provider acceptance of your reservation request.</i>
    </div>
    """, unsafe_allow_html=True)

    if not hotels:
        st.info("No hotels matched your filter criteria.")
        return

    for h in hotels:
        with st.container():
            col1, col2 = st.columns([1.2, 2])
            with col1:
                img = h.get("image_url", "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=700&q=80")
                st.image(img, use_container_width=True)
            with col2:
                st.markdown(f"### {h.get('name')}")
                st.markdown(f"⭐ **{h.get('star_rating', 4)} Stars** &nbsp;|&nbsp; Guest Rating: **{h.get('guest_rating', 4.8)} / 5.0** &nbsp;|&nbsp; 📍 *{h.get('destination')}*")
                st.write(h.get("description", ""))
                st.markdown(f"**Amenities:** {', '.join(h.get('amenities', []))}")
                
                price_inr = h.get("price_per_night", 4500)
                st.markdown(f"<div style='font-size: 1.3rem; font-weight: 800; color: #FB923C; margin-top: 0.5rem;'>{currency_service.format_currency(price_inr, 'INR')} <span style='font-size: 0.9rem; color: #94A3B8; font-weight: normal;'>/ night (est.)</span></div>", unsafe_allow_html=True)
                
                b1, b2 = st.columns(2)
                with b1:
                    if st.button(f"🛎️ Request Booking", key=f"htl_book_{h.get('_id')}", type="primary"):
                        user = st.session_state.get("user") or {}
                        user_id = user.get("_id", "guest_traveler")
                        bkg = create_booking_doc(
                            user_id=user_id,
                            user_name=user.get("full_name", "Traveler"),
                            user_email=user.get("email", "traveler@example.com"),
                            provider_id=h.get("provider_id", "system"),
                            listing_id=h.get("_id"),
                            listing_type="Hotel",
                            listing_name=h.get("name"),
                            dates="Upcoming 3 nights",
                            guests=2,
                            total_price=float(price_inr * 3),
                            currency="INR",
                            status="Pending"
                        )
                        bkg_id = Repository.create_booking(bkg)
                        st.success(f"Reservation request dispatched (ID: {bkg_id})! Provider has been notified.")
                with b2:
                    user = st.session_state.get("user") or {}
                    user_id = user.get("_id", "guest_traveler")
                    if st.button(f"❤️ Save Stay", key=f"htl_fav_{h.get('_id')}"):
                        Repository.toggle_favorite(
                            user_id=user_id,
                            item_id=h.get("_id"),
                            item_type="hotel",
                            title=h.get("name"),
                            image_url=h.get("image_url", ""),
                            destination=h.get("destination"),
                            price_info=f"{currency_service.format_currency(price_inr, 'INR')}/night"
                        )
                        st.success("Hotel bookmarked!")
            st.markdown("---")
