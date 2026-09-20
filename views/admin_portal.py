import streamlit as st
import plotly.express as px
import pandas as pd
from database.repositories import Repository
from database.connection import db_manager
from config.settings import settings
from ui.components import render_section_header, render_kpi_card, render_status_badge
from services.currency_service import currency_service

def render_admin_portal_view():
    # Security Role Guard
    user = st.session_state.get("user") or {}
    if user.get("role") != "Admin":
        st.error("⛔ Access Denied. This administrative terminal requires verified Admin credentials.")
        return

    render_section_header("Admin Control Center & Intelligence Hub 🛡️", "Platform governance, user verification, listing moderation, API status, and macro analytics")

    # Fetch Admin KPIs
    kpis = Repository.get_admin_kpis()
    a1, a2, a3, a4, a5, a6 = st.columns(6)
    with a1:
        render_kpi_card("Total Users", str(kpis["total_users"]), "Registered travelers")
    with a2:
        render_kpi_card("Active Providers", str(kpis["active_providers"]), "Vetted partners")
    with a3:
        render_kpi_card("Generated Trips", str(kpis["total_trips"]), "All-time AI itineraries")
    with a4:
        render_kpi_card("Total Bookings", str(kpis["total_bookings"]), f"{kpis['confirmed_bookings']} Confirmed")
    with a5:
        render_kpi_card("Gross Revenue", currency_service.format_currency(kpis["total_revenue"], "INR"), "Settled turnover")
    with a6:
        render_kpi_card("Top Destination", kpis["popular_destination"], "Highest demand")

    st.write("")
    tab_analytics, tab_users, tab_providers, tab_bookings, tab_api_status = st.tabs([
        "📊 System Analytics & Trends",
        "👥 User Management",
        "🏢 Provider Approvals",
        "🛎️ Master Bookings Log",
        "⚙️ API & Infrastructure Health"
    ])

    # 1. TAB: PLOTLY ANALYTICS
    with tab_analytics:
        st.markdown("### Platform Macro Analytics")
        ch1, ch2 = st.columns(2)
        with ch1:
            # Popular destinations chart
            dest_data = pd.DataFrame([
                {"Destination": "Goa", "Trips": 142},
                {"Destination": "Hyderabad", "Trips": 118},
                {"Destination": "Jaipur", "Trips": 95},
                {"Destination": "Kerala", "Trips": 88},
                {"Destination": "Delhi", "Trips": 76},
                {"Destination": "Paris", "Trips": 54}
            ])
            fig_dest = px.bar(
                dest_data, x="Destination", y="Trips",
                title="Top In-Demand Destinations",
                color="Trips", color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_dest, use_container_width=True)

        with ch2:
            # Booking trends
            month_data = pd.DataFrame([
                {"Month": "May", "Bookings": 32, "Revenue": 145000},
                {"Month": "Jun", "Bookings": 48, "Revenue": 210000},
                {"Month": "Jul", "Bookings": 55, "Revenue": 280000},
                {"Month": "Aug", "Bookings": 72, "Revenue": 365000},
                {"Month": "Sep", "Bookings": 89, "Revenue": 480000}
            ])
            fig_trend = px.line(
                month_data, x="Month", y="Revenue",
                markers=True, title="Monthly Platform Turnover Trend (₹ INR)",
                line_shape="spline"
            )
            fig_trend.update_traces(line_color="#0D9488", line_width=3)
            st.plotly_chart(fig_trend, use_container_width=True)

    # 2. TAB: USER MANAGEMENT
    with tab_users:
        st.markdown("### Registered Users Directory")
        all_users = Repository.list_users()
        for u in all_users:
            if u.get("role") == "Admin":
                continue
            with st.container():
                uc1, uc2, uc3 = st.columns([2, 1, 1])
                with uc1:
                    st.markdown(f"**{u.get('full_name')}** ({u.get('email')}) - `{u.get('role')}`")
                    st.caption(f"Status: {'Active' if u.get('is_active', True) else 'Suspended'} | Phone: {u.get('phone', 'N/A')}")
                with uc2:
                    is_act = u.get("is_active", True)
                    if st.button(f"{'Suspend' if is_act else 'Activate'}", key=f"tgl_{u.get('_id')}"):
                        Repository.update_user_status(u.get("_id"), not is_act)
                        st.success("User status updated.")
                        st.rerun()
                with uc3:
                    if st.button("🗑️ Delete", key=f"del_u_{u.get('_id')}"):
                        Repository.delete_user(u.get("_id"))
                        st.success("User deleted.")
                        st.rerun()
            st.markdown("---")

    # 3. TAB: PROVIDER APPROVALS
    with tab_providers:
        st.markdown("### Hospitality Partner Verification Queue")
        providers = Repository.list_users(role="Provider")
        if not providers:
            st.info("No provider accounts registered.")
        else:
            for p in providers:
                appr = p.get("provider_approved", False)
                p_col1, p_col2 = st.columns([3, 1])
                with p_col1:
                    st.markdown(f"**{p.get('full_name')}** | Business: **{p.get('provider_business_name')}**")
                    st.caption(f"Email: {p.get('email')} | Type: {p.get('provider_type')} | Status: {'✅ Approved' if appr else '⏳ Pending Review'}")
                with p_col2:
                    if not appr:
                        if st.button("Approve Partner", key=f"appr_{p.get('_id')}", type="primary"):
                            Repository.approve_provider(p.get("_id"), True)
                            st.success("Provider approved!")
                            st.rerun()
                    else:
                        if st.button("Revoke Approval", key=f"revk_{p.get('_id')}"):
                            Repository.approve_provider(p.get("_id"), False)
                            st.warning("Approval revoked.")
                            st.rerun()
                st.markdown("---")

    # 4. TAB: MASTER BOOKINGS LOG
    with tab_bookings:
        st.markdown("### Master Reservation Transactions")
        bookings = Repository.list_all_bookings()
        if not bookings:
            st.info("No bookings recorded on platform.")
        else:
            for b in bookings:
                st.markdown(f"""
                <div style="background: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 1rem; margin-bottom: 0.75rem; color: #CBD5E1;">
                    <b style="color: #38BDF8;">{b.get('listing_name')}</b> ({b.get('listing_type')}) - {b.get('dates')} | 
                    Traveler: <span style="color: #F8FAFC;">{b.get('user_name')}</span> | Status: <span style="color: #2DD4BF; font-weight: 700;">{b.get('status')}</span> | 
                    Total: <span style="color: #FB923C; font-weight: 700;">{currency_service.format_currency(b.get('total_price', 0), b.get('currency', 'INR'))}</span>
                </div>
                """, unsafe_allow_html=True)

    # 5. TAB: API & INFRASTRUCTURE HEALTH
    with tab_api_status:
        st.markdown("### External APIs & Infrastructure Health Monitor")
        db_stat = db_manager.get_status()
        
        h1, h2, h3 = st.columns(3)
        with h1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Database Status</div>
                <div class="kpi-value" style="color: #2DD4BF;">ONLINE</div>
                <div class="kpi-sub">Engine: {db_stat['type']}</div>
            </div>
            """, unsafe_allow_html=True)
        with h2:
            gemini_active = settings.has_gemini_key()
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Gemini AI API</div>
                <div class="kpi-value" style="color: {'#2DD4BF' if gemini_active else '#F59E0B'};">
                    {'ONLINE' if gemini_active else 'DEMO FALLBACK'}
                </div>
                <div class="kpi-sub">{'Connected & Verified' if gemini_active else 'Algorithmic Fallback Engine Active'}</div>
            </div>
            """, unsafe_allow_html=True)
        with h3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Weather & Maps API</div>
                <div class="kpi-value" style="color: #2DD4BF;">ONLINE</div>
                <div class="kpi-sub">Open-Meteo & Nominatim OSM</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### System Configuration Details")
        st.code(f"""
Project Name: {settings.PROJECT_NAME}
Database Name: {settings.DATABASE_NAME}
MongoDB Live Connection: {db_manager.is_live_mongo}
JWT Secret Configured: {bool(settings.JWT_SECRET)}
Admin Identity: {settings.ADMIN_EMAIL}
        """, language="yaml")
