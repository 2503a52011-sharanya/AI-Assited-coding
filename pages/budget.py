import streamlit as st
import plotly.express as px
from services.budget_service import BudgetService
from utils.helpers import format_currency


def render_budget_page():
    st.title("💰 Budget Planner & Auto-Optimizer")
    st.caption("Plan transparent travel expenses, avoid hidden surprises, and discover smart savings.")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.number_input("Target Total Budget (₹)", min_value=3000, max_value=500000, value=20000, step=1000)
            days = st.slider("Duration (Days)", min_value=1, max_value=14, value=3)
        with col2:
            travelers = st.slider("Number of Travelers", min_value=1, max_value=10, value=2)
            trans_mode = st.selectbox("Transport Mode", ["Train (3AC / Sleeper)", "Flight", "Intercity Bus", "Outstation Cab"])
        with col3:
            hotel_tier = st.selectbox("Hotel Tier", ["Homestay / Budget Inn (₹1,200/night)", "3-Star Comfort Hotel (₹2,200/night)", "4-Star / Luxury Resort (₹5,500/night)"])
            food_style = st.selectbox("Dining Preference", ["Local food", "Vegetarian", "Non-vegetarian", "Budget food", "Premium restaurants"])

    # Resolve Rates
    t_fare = 500.0
    if "Flight" in trans_mode:
        t_fare = 3500.0
    elif "Bus" in trans_mode:
        t_fare = 950.0
    elif "Cab" in trans_mode:
        t_fare = 3800.0

    h_rate = 1200.0
    if "3-Star" in hotel_tier:
        h_rate = 2200.0
    elif "Luxury" in hotel_tier:
        h_rate = 5500.0

    # Calculate
    calc = BudgetService.calculate_trip_budget(
        days=days,
        travelers=travelers,
        transport_fare_per_person=t_fare,
        hotel_nightly_rate=h_rate,
        food_style=food_style,
        activities_cost_per_person=600.0,
        local_cab_daily_rate=1200.0
    )

    opt = BudgetService.optimize_budget(
        user_budget=budget,
        original_plan=calc,
        days=days,
        travelers=travelers,
        current_transport_type="Flight" if "Flight" in trans_mode else "Train",
        current_hotel_price=h_rate
    )

    st.markdown("---")
    st.subheader("Financial Breakdown")

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Allocated Budget", format_currency(budget))
    with mcol2:
        st.metric("Estimated Cost", format_currency(calc["total_estimated_cost"]))
    with mcol3:
        bal = budget - calc["total_estimated_cost"]
        st.metric("Surplus / Deficit", format_currency(bal), delta=f"{format_currency(bal)}")
    with mcol4:
        st.metric("Per Person", format_currency(calc["cost_per_person"]))

    # Auto Optimization section if over budget
    if opt["needs_optimization"]:
        st.error(f"⚠️ Original plan exceeds your budget by {format_currency(abs(bal))}.")
        st.success(f"💡 **Auto-Optimized Plan Available:** We optimized this trip down to **{format_currency(opt['optimized_plan']['total_estimated_cost'])}**, generating **{format_currency(opt['savings'])}** in realistic savings!")

        st.markdown("### 📊 Side-by-Side Comparison")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("#### ❌ Original Plan")
                st.write(f"- Transportation: {format_currency(opt['original_plan']['transport_cost'])}")
                st.write(f"- Hotel: {format_currency(opt['original_plan']['accommodation_cost'])}")
                st.write(f"- Food: {format_currency(opt['original_plan']['food_cost'])}")
                st.write(f"- Activities: {format_currency(opt['original_plan']['activities_cost'])}")
                st.write(f"- Local Travel: {format_currency(opt['original_plan']['local_transport_cost'])}")
                st.write(f"- Buffer: {format_currency(opt['original_plan']['buffer_cost'])}")
                st.markdown(f"**Total: {format_currency(opt['original_plan']['total_estimated_cost'])}**")

        with c2:
            with st.container(border=True):
                st.markdown("#### ✅ Optimized Plan")
                st.write(f"- Transportation: {format_currency(opt['optimized_plan']['transport_cost'])}")
                st.write(f"- Hotel: {format_currency(opt['optimized_plan']['accommodation_cost'])}")
                st.write(f"- Food: {format_currency(opt['optimized_plan']['food_cost'])}")
                st.write(f"- Activities: {format_currency(opt['optimized_plan']['activities_cost'])}")
                st.write(f"- Local Travel: {format_currency(opt['optimized_plan']['local_transport_cost'])}")
                st.write(f"- Buffer: {format_currency(opt['optimized_plan']['buffer_cost'])}")
                st.markdown(f"**Total: {format_currency(opt['optimized_plan']['total_estimated_cost'])}**")

        st.markdown("##### 🔍 Optimization Recommendations:")
        for r in opt["recommendations"]:
            st.markdown(f"- {r}")

    # Plotly Donut Chart
    active_b = opt["optimized_plan"] if opt["needs_optimization"] else calc
    fig = px.pie(
        values=list(active_b["breakdown_percentages"].values()),
        names=list(active_b["breakdown_percentages"].keys()),
        title="Cost Category Share (%)",
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig, width="stretch")


render_budget_page()

