import streamlit as st
from database.repositories import Repository
from ui.components import render_section_header
from services.currency_service import currency_service
from services.export_service import export_service

def render_my_trips_view():
    render_section_header("My Trips & Itinerary Archive 🧳", "View past journeys, track upcoming expeditions, and download travel packages")

    user = st.session_state.get("user") or {}
    user_id = user.get("_id", "guest_traveler")
    trips = Repository.get_user_trips(user_id)

    if not trips:
        st.info("You haven't planned any trips yet.")
        if st.button("🚀 Plan a New Trip", type="primary"):
            st.session_state.current_page = "Plan My Trip"
            st.rerun()
        return

    for t in trips:
        dest = t.get("destination", "Destination")
        curr = t.get("currency", "INR")
        budget = t.get("budget", 0)
        costs = t.get("estimated_costs", {})
        total_cost = costs.get("total_estimated", 0)
        
        with st.container():
            st.markdown(f"""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.25rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.4rem; font-weight: 800; color: #38BDF8;">{dest} Adventure</span>
                    <span style="background: #0D9488; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 700;">
                        {t.get('status', 'Upcoming')}
                    </span>
                </div>
                <div style="color: #94A3B8; margin-top: 0.4rem; font-size: 0.95rem;">
                    📅 <b>Dates:</b> {t.get('start_date')} to {t.get('end_date')} ({t.get('days')} Days) &nbsp;|&nbsp; 
                    👥 <b>Travelers:</b> {t.get('travelers')} &nbsp;|&nbsp; 
                    🏷️ <b>Style:</b> {t.get('travel_style')}
                </div>
                <div style="display: flex; gap: 24px; margin-top: 0.8rem; margin-bottom: 1rem;">
                    <div><b>Budget:</b> <span style="color: #F8FAFC;">{currency_service.format_currency(budget, curr)}</span></div>
                    <div><b>Estimated Total:</b> <span style="color: #FB923C; font-weight: 800;">{currency_service.format_currency(total_cost, curr)}</span></div>
                    <div><b>Interests:</b> <span style="color: #2DD4BF;">{', '.join(t.get('interests', [])[:3])}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, b3 = st.columns([1, 1, 1])
            with b1:
                if st.button(f"🔎 View Full Itinerary", key=f"view_trip_{t.get('_id')}", use_container_width=True, type="primary"):
                    st.session_state.active_trip = t
                    st.session_state.current_page = "Trip Results"
                    st.rerun()
            with b2:
                try:
                    pdf_bytes = export_service.generate_pdf(t)
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_bytes,
                        file_name=f"Trip_{dest.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"dl_pdf_{t.get('_id')}",
                        use_container_width=True
                    )
                except Exception:
                    st.write("")
            with b3:
                if st.button(f"🗑️ Delete Plan", key=f"del_trip_{t.get('_id')}", use_container_width=True):
                    Repository.delete_trip(t.get("_id"), user_id)
                    st.success("Trip deleted.")
                    st.rerun()
            st.markdown("---")
