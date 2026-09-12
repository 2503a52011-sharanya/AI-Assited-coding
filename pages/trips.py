import streamlit as st
from database.queries import get_user_trips, get_trip_itinerary, get_trip_budget, execute_query
from utils.helpers import format_currency


def render_trips_page():
    st.title("🧳 My Trips")
    st.caption("Manage, view, and modify your saved personal travel itineraries.")

    user_id = st.session_state.get("user_id", 2)
    trips = get_user_trips(user_id)

    if not trips:
        st.info("You don't have any saved trips yet! Head over to 'Plan My Trip' to generate your first journey.")
        if st.button("Start Planning Now", type="primary"):
            st.switch_page("pages/planner.py")
        return

    st.write(f"You have **{len(trips)}** saved trip(s):")

    for t in trips:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1.5])
            with col1:
                st.markdown(f"### {t['trip_name']}")
                st.markdown(f"📍 **{t['origin']} ➔ {t['destination']}**")
                st.caption(f"🗓️ {t['start_date']} to {t['end_date']} ({t['days']} Days, {t['travelers_count']} Traveler(s))")
            with col2:
                st.markdown(f"Budget: **{format_currency(t['allocated_budget'])}**")
                st.markdown(f"Est Cost: **{format_currency(t['total_estimated_cost'])}**")
                diff = t['allocated_budget'] - t['total_estimated_cost']
                st.caption(f"Status: `{t['status']}`")
            with col3:
                st.markdown(f"Traveler Type: `{t['traveler_type']}`")
                st.markdown(f"Style: `{t['travel_style']}`")
            with col4:
                btn_view = st.button("View Itinerary", key=f"v_trip_{t['id']}", width="stretch")

            if btn_view or st.session_state.get(f"view_trip_active_{t['id']}"):
                st.session_state[f"view_trip_active_{t['id']}"] = True
                st.markdown("---")
                st.subheader(f"Schedule for {t['trip_name']}")

                items = get_trip_itinerary(t["id"])
                if items:
                    days_present = sorted(list(set(i["day_number"] for i in items)))
                    for d_num in days_present:
                        st.markdown(f"##### 📌 Day {d_num}")
                        d_items = [i for i in items if i["day_number"] == d_num]
                        for di in d_items:
                            st.markdown(f"- **{di['time_slot']}** — **{di['activity_title']}** ({di['activity_type']}) - *{format_currency(di['estimated_cost'])}*")
                            if di.get("notes"):
                                st.caption(f"  {di['notes']}")
                else:
                    st.info("No detailed items stored for this trip.")

                # Download Trip Summary
                summary_text = (
                    f"TRIP SUMMARY: {t['trip_name']}\n"
                    f"Route: {t['origin']} to {t['destination']}\n"
                    f"Dates: {t['start_date']} to {t['end_date']} ({t['days']} Days)\n"
                    f"Travelers: {t['travelers_count']} ({t['traveler_type']})\n"
                    f"Total Estimated Cost: {format_currency(t['total_estimated_cost'])}\n\n"
                    f"ITINERARY:\n"
                )
                for item in items:
                    summary_text += f"- Day {item['day_number']} | {item['time_slot']} | {item['activity_title']} ({format_currency(item['estimated_cost'])})\n"

                st.download_button(
                    label="📥 Download Trip Summary",
                    data=summary_text,
                    file_name=f"Trip_{t['destination']}_{t['id']}.txt",
                    mime="text/plain",
                    key=f"dl_trip_{t['id']}"
                )


render_trips_page()

