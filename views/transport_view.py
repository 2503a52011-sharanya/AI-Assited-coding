import streamlit as st
from services.transport_service import transport_service
from services.currency_service import currency_service
from ui.components import render_section_header

def render_transport_view():
    render_section_header("Transportation Hub & Route Estimator 🚗", "Compare intercity transit routes, durations, and local city commutation options")

    c1, c2, c3 = st.columns([1.2, 1.2, 0.8])
    with c1:
        origin = st.text_input("Origin Point / City", value="Hyderabad").strip()
    with c2:
        destination = st.text_input("Destination City", value="Goa").strip()
    with c3:
        passengers = st.number_input("Travelers", min_value=1, max_value=20, value=2)

    st.markdown("""
    <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 1rem;">
        ℹ️ <i>Notice: Transit schedules and fares are estimated based on standard operational averages. Real-time booking requires carrier verification.</i>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 Calculate Route Options", type="primary", use_container_width=True):
        st.session_state.transport_calculated = True

    routes = transport_service.get_transport_options(
        start_location=origin,
        destination=destination,
        travelers=passengers,
        currency="INR"
    )

    st.markdown(f"### Intercity Routes: {origin} ➔ {destination}")
    for r in routes:
        total_fare = r.get("total_cost_converted", 0)
        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.25rem; font-weight: 700; color: #38BDF8;">{r.get('type')}</span>
                <span style="font-size: 1.3rem; font-weight: 800; color: #FB923C;">{currency_service.format_currency(total_fare, 'INR')} <span style='font-size: 0.85rem; color: #94A3B8; font-weight: normal;'>({passengers} pax)</span></span>
            </div>
            <p style="color: #CBD5E1; margin-top: 0.3rem; margin-bottom: 0.4rem;">
                ⏱️ <b>Estimated Duration:</b> {r.get('duration')} &nbsp;|&nbsp; 
                ⭐ <b>Convenience:</b> {r.get('convenience')} &nbsp;|&nbsp; 
                🚘 <b>Vehicle Type:</b> {r.get('vehicle_details')}
            </p>
            <div style="font-size: 0.85rem; color: #94A3B8;">{r.get('description')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### 🏙️ Local City Commutation Guide")
    st.markdown("Typical ways to navigate within your destination:")
    local_opts = transport_service.get_local_transit_options(destination=destination, currency="INR")
    l_cols = st.columns(len(local_opts))
    for idx, opt in enumerate(local_opts):
        with l_cols[idx]:
            st.markdown(f"""
            <div style="border: 1px solid #334155; border-radius: 12px; padding: 1rem; background: #1E293B; height: 100%;">
                <div style="font-weight: 700; color: #F8FAFC; font-size: 0.95rem; margin-bottom: 0.3rem;">{opt.get('mode')}</div>
                <div style="color: #2DD4BF; font-weight: 800; font-size: 1.1rem; margin-bottom: 0.4rem;">~{currency_service.format_currency(opt.get('daily_cost_converted', 300), 'INR')} / day</div>
                <div style="font-size: 0.8rem; color: #94A3B8;"><b>Best for:</b> {opt.get('best_for')}</div>
            </div>
            """, unsafe_allow_html=True)
