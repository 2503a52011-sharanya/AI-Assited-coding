import streamlit as st
from database.repositories import Repository
from database.models import (
    create_hotel_doc, create_restaurant_doc,
    create_transport_doc, create_activity_doc
)
from ui.components import render_section_header, render_kpi_card, render_status_badge
from services.currency_service import currency_service

def render_provider_portal_view():
    user = st.session_state.get("user") or {}
    provider_id = user.get("_id", "provider_demo")
    business_name = user.get("provider_business_name", "Taj Stays & Hospitality")

    render_section_header(f"Provider Portal 🏢 - {business_name}", "Manage hospitality listings, accept traveler booking requests, and inspect earnings")

    # Fetch Provider KPIs
    kpis = Repository.get_provider_kpis(provider_id)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Total Listings", str(kpis["total_listings"]), "Active portfolio")
    with k2:
        render_kpi_card("Booking Requests", str(kpis["total_bookings"]), f"{kpis['pending_bookings']} Pending Review")
    with k3:
        render_kpi_card("Confirmed Revenue", currency_service.format_currency(kpis["revenue"], "INR"), "Settled earnings")
    with k4:
        render_kpi_card("Guest Rating", f"★ {kpis['avg_rating']}", "Verified reviews")

    st.write("")
    tab_bookings, tab_listings, tab_add_listing = st.tabs([
        "🛎️ Booking Requests & Confirmations",
        "📋 Active Listings Portfolio",
        "➕ Create New Listing"
    ])

    # 1. TAB: BOOKING REQUESTS (CONFIRM / REJECT WORKFLOW)
    with tab_bookings:
        st.markdown("### Traveler Reservation Inquiries")
        bookings = Repository.get_provider_bookings(provider_id)
        if not bookings:
            st.info("No booking requests received yet.")
        else:
            for b in bookings:
                status = b.get("status", "Pending")
                badge_html = render_status_badge(status)
                st.markdown(f"""
                <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.15rem; font-weight: 700; color: #38BDF8;">{b.get('listing_name')} ({b.get('listing_type')})</span>
                        <div>{badge_html}</div>
                    </div>
                    <div style="color: #94A3B8; margin-top: 0.3rem; font-size: 0.9rem;">
                        👤 <b>Traveler:</b> <span style="color: #F8FAFC;">{b.get('user_name')}</span> ({b.get('user_email')}) &nbsp;|&nbsp; 
                        📅 <b>Dates:</b> {b.get('dates')} &nbsp;|&nbsp; 
                        👥 <b>Guests:</b> {b.get('guests')}
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 1rem; color: #FB923C; font-weight: 800;">
                        Total Value: {currency_service.format_currency(b.get('total_price', 0), b.get('currency', 'INR'))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if status == "Pending":
                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button("✅ Confirm Reservation", key=f"conf_{b.get('_id')}", type="primary"):
                            Repository.update_booking_status(b.get("_id"), "Confirmed", provider_id)
                            st.success("Booking confirmed! Traveler has been notified.")
                            st.rerun()
                    with btn_c2:
                        if st.button("❌ Reject Request", key=f"rej_{b.get('_id')}"):
                            Repository.update_booking_status(b.get("_id"), "Rejected", provider_id)
                            st.warning("Booking rejected.")
                            st.rerun()
                st.markdown("---")

    # 2. TAB: ACTIVE LISTINGS
    with tab_listings:
        st.markdown("### Managed Properties & Services")
        hotels = Repository.list_hotels()
        # Filter for this provider or show demo listings
        my_hotels = [h for h in hotels if h.get("provider_id") == provider_id or h.get("provider_id") == "system"]
        if not my_hotels:
            st.info("No active listings found under your account.")
        else:
            for h in my_hotels:
                with st.container():
                    lc1, lc2 = st.columns([1, 3])
                    with lc1:
                        st.image(h.get("image_url", "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=400&q=80"))
                    with lc2:
                        st.markdown(f"**{h.get('name')}** - *{h.get('room_type')}* ({h.get('destination')})")
                        st.markdown(f"Price: **{currency_service.format_currency(h.get('price_per_night', 0), 'INR')}/night**")
                        if st.button("🗑️ Remove Listing", key=f"del_h_{h.get('_id')}"):
                            Repository.delete_hotel(h.get("_id"), provider_id)
                            st.success("Listing removed.")
                            st.rerun()
                st.markdown("---")

    # 3. TAB: CREATE NEW LISTING
    with tab_add_listing:
        st.markdown("### Add New Property / Service to the Platform")
        listing_type = st.selectbox("Listing Type", ["Hotel", "Restaurant", "Transport", "Tour/Activity"])

        with st.form("form_create_listing"):
            if listing_type == "Hotel":
                h_name = st.text_input("Hotel Name", placeholder="e.g. The Imperial Suites")
                h_dest = st.text_input("Destination City", placeholder="e.g. Goa, Hyderabad")
                h_room = st.text_input("Room Type", placeholder="e.g. Luxury Sea View Deluxe")
                h_price = st.number_input("Price per Night (₹ INR)", min_value=500.0, value=6500.0, step=500.0)
                h_stars = st.slider("Star Rating", 1, 5, 4)
                h_amenities = st.text_input("Amenities (comma separated)", value="WiFi, Breakfast, Swimming Pool, Spa")
                h_image = st.text_input("Image URL", value="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80")
                h_desc = st.text_area("Description", "Experience tranquil hospitality and world-class luxury.")

            elif listing_type == "Restaurant":
                h_name = st.text_input("Restaurant Name", placeholder="e.g. Coastal Spice Bistro")
                h_dest = st.text_input("Destination City", placeholder="e.g. Goa")
                h_room = st.text_input("Cuisine Type", placeholder="e.g. Seafood & Goan")
                h_price = st.number_input("Average Meal Cost per Person (₹ INR)", min_value=100.0, value=900.0, step=100.0)
                h_stars = 4
                h_amenities = st.text_input("Opening Hours", value="11:30 AM - 11:00 PM")
                h_image = st.text_input("Image URL", value="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80")
                h_desc = st.text_area("Description", "Specializing in fresh local seafood recipes.")

            elif listing_type == "Transport":
                h_name = st.selectbox("Transport Category", ["Flight", "Train", "Taxi / Private Cab", "Bus"])
                h_dest = st.text_input("Route Origin ➔ Destination", placeholder="e.g. Hyderabad to Goa")
                h_room = st.text_input("Duration", value="1h 30m")
                h_price = st.number_input("Price per Passenger (₹ INR)", min_value=200.0, value=3500.0, step=200.0)
                h_stars = 4
                h_amenities = st.text_input("Vehicle Details", value="AC Sedan / SUV")
                h_image = ""
                h_desc = st.text_area("Description", "Comfortable, safe, and punctual transfer.")

            else:  # Tour/Activity
                h_name = st.text_input("Activity Name", placeholder="e.g. Sunset Backwater Kayaking")
                h_dest = st.text_input("Destination", placeholder="e.g. Kerala")
                h_room = st.text_input("Category", value="Adventure & Water Sports")
                h_price = st.number_input("Price per Person (₹ INR)", min_value=200.0, value=1500.0, step=100.0)
                h_stars = 5
                h_amenities = st.text_input("Duration", value="2.5 Hours")
                h_image = st.text_input("Image URL", value="https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=800&q=80")
                h_desc = st.text_area("Description", "Scenic kayaking through tranquil backwater lagoons.")

            submit_listing = st.form_submit_button("Publish Listing to Platform", use_container_width=True, type="primary")

            if submit_listing:
                if not h_name or not h_dest:
                    st.error("Name and Destination are required.")
                else:
                    if listing_type == "Hotel":
                        doc = create_hotel_doc(
                            name=h_name,
                            destination=h_dest,
                            room_type=h_room,
                            price_per_night=h_price,
                            star_rating=h_stars,
                            amenities=[a.strip() for a in h_amenities.split(",")],
                            image_url=h_image,
                            description=h_desc,
                            provider_id=provider_id
                        )
                        Repository.add_hotel(doc)
                    elif listing_type == "Restaurant":
                        doc = create_restaurant_doc(
                            name=h_name,
                            destination=h_dest,
                            cuisine=h_room,
                            avg_cost=h_price,
                            image_url=h_image,
                            description=h_desc,
                            provider_id=provider_id
                        )
                        Repository.add_restaurant(doc)
                    elif listing_type == "Transport":
                        parts = h_dest.split("to")
                        from_l = parts[0].strip() if len(parts) > 1 else "Origin"
                        to_l = parts[1].strip() if len(parts) > 1 else h_dest
                        doc = create_transport_doc(
                            transport_type=h_name,
                            from_loc=from_l,
                            to_loc=to_l,
                            estimated_cost=h_price,
                            duration=h_room,
                            vehicle_details=h_amenities,
                            description=h_desc,
                            provider_id=provider_id
                        )
                        Repository.add_transport(doc)
                    else:
                        doc = create_activity_doc(
                            name=h_name,
                            destination=h_dest,
                            category=h_room,
                            price=h_price,
                            duration=h_amenities,
                            image_url=h_image,
                            description=h_desc,
                            provider_id=provider_id
                        )
                        Repository.get_db_collection("activities").insert_one(doc)

                    st.success(f"🎉 Listing '{h_name}' published successfully!")
                    st.rerun()
