import streamlit as st
from datetime import date, timedelta
from database.queries import fetch_all, execute_query
from services.destination_service import DestinationService
from services.booking_service import BookingService
from utils.helpers import format_currency


def render_hostels_page():
    st.title("🛏️ Backpacker Hostel & Dorms Dashboard")
    st.caption("Discover verified youth hostels, reserve cozy dorm beds, and connect with global travelers.")

    # Top Metrics Row
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Verified Hostels", "12+")
    with mcol2:
        st.metric("Beds Available Tonight", "148 Beds")
    with mcol3:
        st.metric("Dorm Beds From", "₹450 / night")
    with mcol4:
        st.metric("Community Wi-Fi Rating", "4.8 / 5.0 ⭐")

    st.markdown("---")

    tab_search, tab_manager, tab_community = st.tabs([
        "🔍 Find & Reserve Beds", "🏢 Hostel Reception & Manager", "🎉 Hostel Events & Community"
    ])

    with tab_search:
        # Search & Filter Bar
        destinations = DestinationService.get_all(limit=100)
        dest_names = ["All Destinations"] + [d["name"] for d in destinations]

        fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
        with fcol1:
            sel_dest = st.selectbox("Select Destination", dest_names, index=0, key="hostel_dest_choice")
        with fcol2:
            dorm_filter = st.selectbox("Dorm Room Preference", [
                "All Dorm Types",
                "Mixed Dormitory (6-8 Beds)",
                "Female Only Dorm (4-6 Beds)",
                "Private Pod Bed",
                "Private Room for 2"
            ], key="hostel_dorm_filter")
        with fcol3:
            max_bed_price = st.slider("Max Bed Price (₹/night)", 300, 2500, 1000, step=50, key="hostel_price_slider")

        # Fetch hostels from database
        query = "SELECT * FROM hotels WHERE (hotel_type = 'Hostel' OR hotel_type = 'Homestay') AND price_per_night <= :max_p"
        params = {"max_p": float(max_bed_price)}
        if sel_dest != "All Destinations":
            dest_match = next((d for d in destinations if d["name"] == sel_dest), None)
            if dest_match:
                query += " AND destination_id = :did"
                params["did"] = dest_match["id"]

        query += " ORDER BY rating DESC"
        hostels = fetch_all(query, params)

        st.write(f"Showing **{len(hostels)}** verified backpacker hostel(s):")

        if not hostels:
            st.info("No hostels found matching your exact filter. Try increasing the price slider or choosing another destination.")
        else:
            for h in hostels:
                with st.container(border=True):
                    c_img, c_info, c_book = st.columns([1.5, 2.8, 1.7])
                    with c_img:
                        st.image(h.get("image_url") or "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800", width="stretch")
                    with c_info:
                        st.markdown(f"### {h['name']}")
                        st.markdown(f"⭐ **{h['rating']}/5.0 Backpacker Rating** | `{h.get('hotel_type', 'Hostel')}`")
                        st.caption(f"📍 {h.get('address', 'City Center')}")
                        st.markdown(f"✨ **Hostel Perks:** *{h.get('amenities', 'Free Wi-Fi, Lockers, Cafe')}*")
                        st.markdown("🛏️ **Dorm Specs:** *Air-conditioned, reading light, charging socket, personal privacy curtain.*")
                    with c_book:
                        st.markdown(f"### {format_currency(h['price_per_night'])}")
                        st.caption("per dorm bed / night (all inclusive)")
                        if st.button("Reserve Bed", key=f"btn_res_bed_{h['id']}", type="primary", width="stretch"):
                            st.session_state["active_hostel_booking"] = h
                            st.rerun()

        # In-page Bed Reservation Modal
        if st.session_state.get("active_hostel_booking"):
            hostel = st.session_state["active_hostel_booking"]
            st.markdown("---")
            with st.container(border=True):
                st.markdown(f"### 🛏️ Instant Bed Reservation: **{hostel['name']}**")
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    bed_type = st.selectbox(
                        "Select Bed / Dorm Type",
                        ["Bunk Bed in Mixed Dorm", "Bunk Bed in Female-Only Dorm", "Single Cozy Pod Bed", "Private Twin Room"],
                        key="modal_bed_type"
                    )
                    num_beds = st.number_input("Number of Beds", min_value=1, max_value=8, value=1, step=1, key="modal_num_beds")
                    num_nights = st.number_input("Duration (Nights)", min_value=1, max_value=30, value=2, step=1, key="modal_num_nights")
                with r_col2:
                    lead_traveler = st.text_input("Lead Traveler Name", value=st.session_state.get("user_name", "Rohit Sharma"), key="modal_lead_name")
                    phone_num = st.text_input("Contact Phone Number", value="+91 9876543210", key="modal_phone")
                    checkin_date = st.date_input("Check-In Date", value=date.today() + timedelta(days=3), key="modal_checkin_date")

                total_amount = float(hostel["price_per_night"]) * num_beds * num_nights
                st.markdown(f"**Total Payable Amount:** **{format_currency(total_amount)}** ({num_beds} Bed(s) × {num_nights} Night(s))")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("💳 Confirm & Lock My Bed", type="primary", width="stretch", key="modal_confirm_bed"):
                        user_id = st.session_state.get("user_id", 2)
                        res = BookingService.book_ticket(
                            user_id=user_id,
                            category="Hostel",
                            provider_name=hostel["name"],
                            item_title=f"{hostel['name']} ({num_beds} Bed(s), {bed_type})",
                            travel_date=str(checkin_date),
                            passenger_count=num_beds,
                            total_amount=total_amount,
                            passengers=[{"name": lead_traveler, "age": 24, "seat": f"Bed {i+1} ({bed_type[:10]})"} for i in range(num_beds)],
                            payment_method="Demo UPI / Hostel Pay at Desk"
                        )
                        st.success(f"🎉 **Bed Reservation Confirmed!** Your Hostel PNR: **`{res['booking_reference']}`**")
                        st.session_state["active_hostel_booking"] = None
                        st.balloons()
                with b2:
                    if st.button("Cancel Reservation", width="stretch", key="modal_cancel_bed"):
                        st.session_state["active_hostel_booking"] = None
                        st.rerun()

    with tab_manager:
        st.subheader("🏢 Hostel Front Desk & Occupancy Tracker")
        st.caption("Real-time view of booked beds, check-ins, and hostel guest log.")

        # Live bookings under Hostel category
        hostel_bookings = fetch_all("""
            SELECT b.*, u.name as user_name, u.email as user_email
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            WHERE b.category = 'Hostel' OR b.provider_name LIKE '%Hostel%' OR b.provider_name LIKE '%Zostel%'
            ORDER BY b.created_at DESC
        """)

        oc1, oc2, oc3 = st.columns(3)
        with oc1:
            st.metric("Total Active Hostel Bookings", len(hostel_bookings))
        with oc2:
            checked_in = sum(1 for b in hostel_bookings if b["status"] == "Confirmed")
            st.metric("Confirmed Stays", checked_in)
        with oc3:
            total_rev = sum(float(b["total_amount"]) for b in hostel_bookings)
            st.metric("Hostel Revenue", format_currency(total_rev))

        st.markdown("##### 📋 Backpacker Guest Log")
        if not hostel_bookings:
            st.info("No hostel guest reservations yet. Book a bed in the 'Find & Reserve Beds' tab to see it logged here!")
        else:
            for hb in hostel_bookings:
                with st.container(border=True):
                    gcol1, gcol2, gcol3 = st.columns([3, 2, 1.5])
                    with gcol1:
                        st.markdown(f"**Hostel:** {hb['provider_name']}")
                        st.markdown(f"**Room & Bed:** `{hb['item_title']}`")
                        st.caption(f"Ref / PNR: `{hb['booking_reference']}` | Guest: {hb.get('user_name', 'Traveler')}")
                    with gcol2:
                        st.markdown(f"Check-In Date: **{hb['travel_date']}**")
                        st.markdown(f"Beds Booked: **{hb['passenger_count']}**")
                        st.caption(f"Total: {format_currency(hb['total_amount'])}")
                    with gcol3:
                        st.markdown(f"Status: **`{hb['status']}`**")
                        if hb["status"] == "Confirmed":
                            st.success("✅ Ready for Check-in")

    with tab_community:
        st.subheader("🎉 Hostel Community Hub & Meetups")
        st.caption("Hostels are about friendships! Check out weekly community events happening at partner properties.")

        events = [
            {"title": "🎸 Rooftop Acoustic Jam & Campfire", "location": "Zostel Araku Valley", "time": "Every Evening, 7:30 PM", "cost": "Free for Guests"},
            {"title": "☕ Specialty Araku Coffee Tasting & Farm Walk", "location": "Araku Valley", "time": "Tomorrow, 8:00 AM", "cost": "₹150 / Person"},
            {"title": "🍕 Hyderabad Street Food Crawl & Biryani Trail", "location": "goSTOPS Hyderabad", "time": "Friday, 6:00 PM", "cost": "Self-paid food"},
            {"title": "🎲 Backpacker Board Games & Mafia Night", "location": "The Hosteller Jubilee Hills", "time": "Saturday, 8:30 PM", "cost": "Free"}
        ]

        for ev in events:
            with st.container(border=True):
                ec1, ec2 = st.columns([3, 1])
                with ec1:
                    st.markdown(f"#### {ev['title']}")
                    st.markdown(f"📍 **Hostel/Location:** {ev['location']} | ⏰ **Time:** `{ev['time']}`")
                with ec2:
                    st.markdown(f"**Entry:** `{ev['cost']}`")
                    st.button("RSVP Event", key=f"rsvp_{ev['title'][:10]}", width="stretch")


render_hostels_page()
