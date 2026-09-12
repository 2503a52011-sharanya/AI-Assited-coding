import streamlit as st
from datetime import date, timedelta
from services.destination_service import DestinationService
from services.hotel_service import HotelService
from services.booking_service import BookingService
from config.settings import ACCOMMODATION_TYPES
from utils.helpers import format_currency


def render_hotels_page():
    st.title("🏨 Accommodations & Stays")
    st.caption("Browse and book scenic resorts, traditional homestays, and verified budget hotels.")

    destinations = DestinationService.get_all(limit=100)
    dest_names = [d["name"] for d in destinations]
    
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.5])
    with col1:
        sel_dest = st.selectbox("Destination", dest_names, index=0, key="hotel_dest_sel")
    with col2:
        hotel_type = st.selectbox("Type", ["All"] + ACCOMMODATION_TYPES, key="hotel_type_sel")
    with col3:
        max_rate = st.slider("Max Nightly Rate (₹)", 800, 15000, 6000, step=500)
    with col4:
        min_star = st.selectbox("Min Star Rating", [1, 2, 3, 4, 5], index=1)

    dest_obj = next((d for d in destinations if d["name"] == sel_dest), destinations[0])
    hotels = HotelService.search_hotels(dest_obj["id"], max_price=max_rate, hotel_type=hotel_type, min_rating=float(min_star))

    st.write(f"Showing **{len(hotels)}** available accommodation(s) in **{sel_dest}**:")

    # Hotel cards
    for h in hotels:
        with st.container(border=True):
            hcol1, hcol2, hcol3 = st.columns([1.5, 3, 1.5])
            with hcol1:
                st.image(h["image_url"], width="stretch")
            with hcol2:
                st.markdown(f"### {h['name']}")
                st.markdown(f"⭐ **{h['star_rating']}-Star {h['hotel_type']}** | Guest Rating: `{h['rating']}/5.0`")
                st.caption(f"📍 {h['address']}")
                st.write(f"✨ Amenities: *{', '.join(h['amenities'])}*")
            with hcol3:
                st.markdown(f"### {format_currency(h['price_per_night'])}")
                st.caption("per night (taxes included)")
                if st.button("Reserve Stay", key=f"bk_htl_{h['id']}", type="primary", width="stretch"):
                    st.session_state["active_hotel_booking"] = h
                    st.rerun()

    # In-App Booking Modal
    if "active_hotel_booking" in st.session_state and st.session_state["active_hotel_booking"]:
        hotel = st.session_state["active_hotel_booking"]
        with st.container(border=True):
            st.markdown(f"### 🛏️ Reserve Your Room: {hotel['name']}")
            nights = st.number_input("Number of Nights", min_value=1, max_value=30, value=2, step=1)
            rooms = st.number_input("Rooms", min_value=1, max_value=10, value=1, step=1)
            total_bill = float(hotel["price_per_night"]) * nights * rooms
            
            st.markdown(f"**Total Payable:** **{format_currency(total_bill)}** for {nights} night(s)")
            guest_name = st.text_input("Lead Guest Name", value=st.session_state.get("user_name", "Rohit Sharma"), key="htl_guest_name")
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("💳 Pay & Confirm Hotel Reservation", type="primary", width="stretch"):
                    user_id = st.session_state.get("user_id", 2)
                    res = BookingService.book_ticket(
                        user_id=user_id,
                        category="Hotel",
                        provider_name=hotel["name"],
                        item_title=f"{hotel['name']} ({nights} Nights, {rooms} Room)",
                        travel_date=str(date.today() + timedelta(days=5)),
                        passenger_count=rooms * 2,
                        total_amount=total_bill,
                        passengers=[{"name": guest_name, "age": 30, "seat": f"Room {101 + rooms}"}],
                        payment_method="Demo UPI Gateway"
                    )
                    st.success(f"🎉 Reservation Confirmed! Booking ID: **`{res['booking_reference']}`**")
                    st.session_state["active_hotel_booking"] = None
                    st.balloons()
            with b_col2:
                if st.button("Cancel Reservation", width="stretch"):
                    st.session_state["active_hotel_booking"] = None
                    st.rerun()


render_hotels_page()

