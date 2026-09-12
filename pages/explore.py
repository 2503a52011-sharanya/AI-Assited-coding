import streamlit as st
from services.destination_service import DestinationService
from config.settings import INTEREST_CATEGORIES
from utils.helpers import format_currency


def render_explore_page():
    st.title("🌍 Explore Diverse Destinations")
    st.caption("From celebrated heritage landmarks to secluded hill retreats and rural hamlets across India.")

    destinations = DestinationService.get_all(limit=100)
    
    # Filter Row
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)
    
    # State list
    states = sorted(list(set(d["state"] for d in destinations if d.get("state"))))
    with fcol1:
        sel_state = st.selectbox("Filter by State", ["All States"] + states)
    
    with fcol2:
        max_budget = st.slider("Max Daily Budget (₹)", 1000, 10000, 8000, step=500)

    with fcol3:
        sel_interest = st.selectbox("Interest Category", ["All Interests"] + INTEREST_CATEGORIES)

    with fcol4:
        sel_duration = st.selectbox("Duration", ["Any Duration", "1-2 Days", "3-4 Days", "5+ Days"])

    # Filter application
    filtered = []
    for d in destinations:
        if sel_state != "All States" and d["state"] != sel_state:
            continue
        if float(d.get("avg_daily_budget", 3000)) > max_budget:
            continue
        if sel_interest != "All Interests":
            tags = (d.get("tags") or "").lower()
            if sel_interest.lower() not in tags:
                continue
        days = int(d.get("ideal_duration_days", 3))
        if sel_duration == "1-2 Days" and days > 2:
            continue
        elif sel_duration == "3-4 Days" and (days < 3 or days > 4):
            continue
        elif sel_duration == "5+ Days" and days < 5:
            continue
        filtered.append(d)

    st.write(f"Showing **{len(filtered)}** destination(s):")

    # Grid Display
    cols = st.columns(3)
    for idx, d in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(d.get("image_url") or "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800", width="stretch")
                st.subheader(d["name"])
                st.markdown(f"📍 **{d['state']}** | ⏱️ `{d.get('ideal_duration_days', 3)} Days`")
                st.markdown(f"💰 Avg: **{format_currency(d.get('avg_daily_budget', 3000.0))}**/day")
                st.caption(d.get("description", "")[:120] + "...")
                
                # Tags pills
                tags = [t.strip() for t in (d.get("tags") or "").split(",") if t.strip()]
                if tags:
                    st.markdown(" ".join([f"`{t}`" for t in tags[:3]]))
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("Details", key=f"exp_det_{d['id']}", width="stretch"):
                        st.session_state["selected_dest_id"] = d["id"]
                        st.switch_page("pages/destinations.py")
                with btn_col2:
                    if st.button("Plan Trip", key=f"exp_plan_{d['id']}", type="primary", width="stretch"):
                        st.session_state["selected_destination_name"] = d["name"]
                        st.switch_page("pages/planner.py")


render_explore_page()

