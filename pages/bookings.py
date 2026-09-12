import streamlit as st
from services.booking_service import BookingService
from utils.helpers import format_currency


def render_bookings_page():
    st.title("🎫 Central Booking Dashboard & Digital Passes")
    st.caption("Real-time management dashboard for all your flights, trains, buses, cabs, hotels, hostels, and activity tickets.")

    user_id = st.session_state.get("user_id", 2)
    all_user_bookings = BookingService.get_user_bookings(user_id, category=None)

    # Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    total_count = len(all_user_bookings)
    confirmed_count = sum(1 for b in all_user_bookings if b["status"] == "Confirmed")
    cancelled_count = sum(1 for b in all_user_bookings if b["status"] == "Cancelled")
    total_spent = sum(float(b["total_amount"]) for b in all_user_bookings if b["status"] == "Confirmed")

    with m1:
        st.metric("Total Bookings", total_count)
    with m2:
        st.metric("Confirmed Active Passes", confirmed_count)
    with m3:
        st.metric("Total Spend", format_currency(total_spent))
    with m4:
        st.metric("Cancelled Bookings", cancelled_count)

    st.markdown("---")

    # Search & Filter Controls
    scol1, scol2, scol3 = st.columns([2.5, 2, 1.5])
    with scol1:
        search_kw = st.text_input("🔍 Search Bookings (PNR, Provider, Title)", placeholder="e.g. STR-, IndiGo, Express...", key="bk_search_kw")
    with scol2:
        cat_filter = st.selectbox("Category", ["All", "Train", "Bus", "Flight", "Hotel", "Hostel", "Cab", "Activity"], index=0, key="bk_cat_sel")
    with scol3:
        status_filter = st.selectbox("Status", ["All", "Confirmed", "Cancelled"], index=0, key="bk_status_sel")

    # Filter bookings
    filtered_bookings = all_user_bookings
    if cat_filter != "All":
        filtered_bookings = [b for b in filtered_bookings if b.get("category", "").lower() == cat_filter.lower()]
    if status_filter != "All":
        filtered_bookings = [b for b in filtered_bookings if b.get("status", "").lower() == status_filter.lower()]
    if search_kw:
        kw = search_kw.lower().strip()
        filtered_bookings = [
            b for b in filtered_bookings
            if kw in b.get("booking_reference", "").lower()
            or kw in b.get("provider_name", "").lower()
            or kw in b.get("item_title", "").lower()
        ]

    st.write(f"Showing **{len(filtered_bookings)}** booking record(s):")

    if not filtered_bookings:
        st.info("No bookings match your current criteria. Use the Planner, Transportation, Hotels, or Hostel Dashboard to book your travel!")
        return

    for b in filtered_bookings:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1.5])
            with col1:
                st.markdown(f"### {b['item_title']}")
                st.markdown(f"🏷️ Category: `{b['category']}` | Provider: **{b['provider_name']}**")
                st.caption(f"Ref / PNR: `{b['booking_reference']}`")
            with col2:
                st.markdown(f"**Travel Date:** {b['travel_date']}")
                st.markdown(f"Guests / Seats: **{b['passenger_count']}**")
            with col3:
                st.markdown(f"Amount Paid: **{format_currency(b['total_amount'])}**")
                status_color = "🟢" if b["status"] == "Confirmed" else "🔴"
                st.markdown(f"Status: {status_color} **{b['status']}**")
                if b.get("is_demo"):
                    st.caption("🔒 Verified Secure Booking")
            with col4:
                btn_ticket = st.button("View Digital Pass", key=f"tkt_{b['id']}", width="stretch")
                if b["status"] == "Confirmed":
                    if st.button("Cancel Pass", key=f"cnl_{b['id']}", width="stretch"):
                        BookingService.cancel_ticket(b["id"], user_id)
                        st.warning("Booking has been cancelled.")
                        st.rerun()

            # Digital Boarding Pass / Ticket Expander
            if btn_ticket or st.session_state.get(f"show_ticket_{b['id']}"):
                st.session_state[f"show_ticket_{b['id']}"] = True
                st.markdown("""
                <div style="background: #ffffff; border: 2px dashed #0284c7; border-radius: 12px; padding: 20px; margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">
                        <span style="font-weight: 700; color: #0369a1; font-size: 1.1rem;">✈️ SMART TOURISM OFFICIAL DIGITAL PASS</span>
                        <span style="font-family: monospace; font-size: 1rem; color: #334155;">PNR / REF: <b>""" + b['booking_reference'] + """</b></span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                        <div>
                            <div style="color: #64748b; font-size: 0.85rem;">SERVICE / ITEM</div>
                            <div style="font-weight: 600; font-size: 1rem;">""" + b['item_title'] + """</div>
                            <div style="color: #64748b; font-size: 0.85rem; margin-top: 8px;">PROVIDER</div>
                            <div style="font-weight: 600;">""" + b['provider_name'] + """</div>
                        </div>
                        <div>
                            <div style="color: #64748b; font-size: 0.85rem;">DATE OF JOURNEY</div>
                            <div style="font-weight: 600;">""" + str(b['travel_date']) + """</div>
                            <div style="color: #64748b; font-size: 0.85rem; margin-top: 8px;">PASSENGERS / GUESTS</div>
                            <div style="font-weight: 600;">""" + str(b['passenger_count']) + """ Person(s)</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #64748b; font-size: 0.85rem;">TOTAL PAID</div>
                            <div style="font-size: 1.2rem; font-weight: 700; color: #047857;">""" + format_currency(b['total_amount']) + """</div>
                            <div style="margin-top: 8px; font-family: monospace; font-size: 1.5rem; letter-spacing: 2px;">||||||||||||||</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


render_bookings_page()

