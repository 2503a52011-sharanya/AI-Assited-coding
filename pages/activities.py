import streamlit as st
from services.destination_service import DestinationService
from services.activity_service import ActivityService
from services.booking_service import BookingService
from utils.helpers import format_currency


def render_activities_page():
    st.title("🧗 Activities & Experiences")
    st.caption("Book guided trekking safaris, cultural folk shows, plantation walks, and museum passes.")

    destinations = DestinationService.get_all(limit=100)
    dest_names = [d["name"] for d in destinations]
    sel_dest = st.selectbox("Select Destination", dest_names, index=0, key="act_dest_sel")

    dest_obj = next((d for d in destinations if d["name"] == sel_dest), destinations[0])
    activities = ActivityService.get_destination_activities(dest_obj["id"])

    st.subheader(f"Curated Experiences in {sel_dest} ({len(activities)})")
    if activities:
        for act in activities:
            with st.container(border=True):
                acol1, acol2, acol3 = st.columns([3, 1.5, 1.5])
                with acol1:
                    st.markdown(f"### {act['title']}")
                    st.markdown(f"🏷️ Category: `{act['category']}` | Suitable for: **{act['suitable_for']}**")
                    st.write(act["description"])
                with acol2:
                    st.markdown(f"⏱️ **{act['duration_hours']} Hours**")
                    st.markdown(f"⭐ **{act['rating']}/5.0**")
                with acol3:
                    st.markdown(f"### {format_currency(act['price_per_person'])}")
                    st.caption("per person")
                    if st.button("Book Experience", key=f"bk_act_{act['id']}", type="primary", width="stretch"):
                        st.session_state["active_activity_booking"] = act
                        st.rerun()
    else:
        st.info(f"No specific paid activities registered yet for {sel_dest}.")

    # In-App Booking Modal
    if "active_activity_booking" in st.session_state and st.session_state["active_activity_booking"]:
        act = st.session_state["active_activity_booking"]
        with st.container(border=True):
            st.markdown(f"### 🎟️ Book Experience: {act['title']}")
            participants = st.number_input("Number of Participants", min_value=1, max_value=20, value=2, step=1)
            total_bill = float(act["price_per_person"]) * participants
            st.markdown(f"**Total Amount:** **{format_currency(total_bill)}**")

            p_name = st.text_input("Lead Participant Name", value=st.session_state.get("user_name", "Rohit Sharma"), key="act_p_name")
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("💳 Confirm Activity Booking", type="primary", width="stretch"):
                    user_id = st.session_state.get("user_id", 2)
                    res = BookingService.book_ticket(
                        user_id=user_id,
                        category="Activity",
                        provider_name=f"{sel_dest} Tourism Experiences",
                        item_title=f"{act['title']} ({participants} Guests)",
                        travel_date="2026-09-15",
                        passenger_count=participants,
                        total_amount=total_bill,
                        passengers=[{"name": p_name, "age": 28, "seat": "Confirmed Pass"}],
                        payment_method="Demo UPI Gateway"
                    )
                    st.success(f"🎉 Activity Pass Confirmed! Ref: **`{res['booking_reference']}`**")
                    st.session_state["active_activity_booking"] = None
                    st.balloons()
            with b_col2:
                if st.button("Cancel", width="stretch"):
                    st.session_state["active_activity_booking"] = None
                    st.rerun()


render_activities_page()

