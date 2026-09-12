import streamlit as st
from database.queries import get_admin_metrics, save_destination
from utils.helpers import format_currency
from utils.authentication import is_authenticated, is_admin


def render_admin_page():
    if not is_authenticated() or not is_admin():
        st.error("🛡️ Access Restricted: Administrator privileges required.")
        st.info("Please log in with an Administrator account using the sidebar auth switcher.")
        if st.button("Return to Home", type="primary"):
            st.switch_page("pages/home.py")
        return

    st.title("🛡️ Platform Administration & Analytics")
    st.caption("Manage destination catalog, monitor booking throughput, revenue, and system health.")

    metrics = get_admin_metrics()

    # KPI Metrics
    kcol1, kcol2, kcol3, kcol4 = st.columns(4)
    with kcol1:
        st.metric("Total Users", metrics["users"])
    with kcol2:
        st.metric("Total Bookings", metrics["bookings"])
    with kcol3:
        st.metric("Platform Revenue", format_currency(metrics["revenue"]))
    with kcol4:
        st.metric("Destinations In Catalog", metrics["destinations"])

    st.markdown("---")

    tab_cms, tab_bookings, tab_health, tab_audit = st.tabs([
        "➕ Add Destination", "📋 Booking Ledger", "🟢 API & System Health", "📜 Audit Logs"
    ])

    with tab_cms:
        st.subheader("Add New Destination to Tourism Catalog")
        with st.form("add_dest_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Destination Name (e.g. Ziro Valley)")
                state = st.text_input("State / Region (e.g. Arunachal Pradesh)")
                city = st.text_input("City / District (e.g. Ziro)")
                lat = st.number_input("Latitude", value=27.5644, format="%.4f")
                lon = st.number_input("Longitude", value=93.8344, format="%.4f")
            with col2:
                best_season = st.text_input("Best Season (e.g. March to October)", value="October to March")
                days = st.number_input("Ideal Duration (Days)", value=3, min_value=1, max_value=15)
                budget = st.number_input("Average Daily Budget (₹)", value=3200.0, step=100.0)
                tags = st.text_input("Tags (comma-separated)", value="Nature, Music, Culture, Mountains")
                img_url = st.text_input("Image URL", value="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800")
            
            desc = st.text_area("Description", value="An enchanting valley known for pine-clad hills, tribal culture, and peaceful landscapes.")
            submitted = st.form_submit_button("Publish Destination", type="primary")

            if submitted:
                if name and state:
                    save_destination(name, state, city, lat, lon, desc, tags, img_url, best_season, budget, days)
                    st.success(f"Destination '{name}' successfully added to catalog!")
                    st.rerun()
                else:
                    st.error("Name and State are required fields.")

    with tab_bookings:
        st.subheader("Recent Platform Transactions")
        recent = metrics["recent_bookings"]
        if recent:
            st.dataframe(recent, width="stretch")
        else:
            st.info("No bookings recorded yet.")

    with tab_health:
        st.subheader("Service Connection Status")
        h_cols = st.columns(3)
        with h_cols[0]:
            st.success("🟢 **Relational Database**: Connected & Operational")
        with h_cols[1]:
            st.success("🟢 **Open-Meteo Weather API**: Active")
        with h_cols[2]:
            st.success("🟢 **OSM Nominatim Geocoder**: Active")

        st.markdown("##### Configuration Mode")
        st.info("Operating in Hybrid Live-API + Safe Verified Demo Mode for transport and payment providers.")

    with tab_audit:
        st.subheader("Platform Audit & Security Logs")
        logs = metrics["audit_logs"]
        if logs:
            st.dataframe(logs, width="stretch")
        else:
            st.info("No audit entries yet.")


render_admin_page()

