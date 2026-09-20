import streamlit as st
import plotly.express as px
from ui.components import render_section_header, render_kpi_card
from services.currency_service import currency_service

def render_budget_view():
    render_section_header("Budget Analytics & AI Cost Optimizer 💰", "Track category expenditure, inspect utilization percentages, and test instant cost-saving substitutions")

    trip = st.session_state.get("active_trip")
    if not trip:
        st.info("No active trip loaded. You can model a scenario below or load a trip from 'My Trips'.")
        total_budget = 35000.0
        currency = "INR"
        costs = {
            "transportation": 8500.0,
            "accommodation": 16000.0,
            "food": 7500.0,
            "activities": 4500.0,
            "local_travel": 2500.0,
            "miscellaneous": 1500.0
        }
    else:
        total_budget = trip.get("budget", 35000.0)
        currency = trip.get("currency", "INR")
        costs = trip.get("estimated_costs", {})

    total_cost = sum([
        costs.get("transportation", 0),
        costs.get("accommodation", 0),
        costs.get("food", 0),
        costs.get("activities", 0),
        costs.get("local_travel", 0),
        costs.get("miscellaneous", 0)
    ])
    remaining = round(total_budget - total_cost, 2)
    utilization = round((total_cost / total_budget) * 100, 1) if total_budget > 0 else 100
    is_over = total_cost > total_budget

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Allocated Budget", currency_service.format_currency(total_budget, currency))
    with k2:
        render_kpi_card("Estimated Spend", currency_service.format_currency(total_cost, currency))
    with k3:
        status_text = "Over Budget" if is_over else "Surplus"
        render_kpi_card(status_text, currency_service.format_currency(abs(remaining), currency), "Deficit" if is_over else "Remaining Balance")
    with k4:
        render_kpi_card("Budget Utilization", f"{utilization}%", "Optimal: 85% - 95%")

    st.write("")
    # Interactive Optimization Sandbox
    with st.expander("🛠️ Interactive AI Budget Optimization Sandbox", expanded=is_over):
        st.markdown("Adjust expense levers below to recalculate spending in real-time:")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            hotel_tier = st.selectbox("Accommodation Tier", ["Luxury (5-Star)", "Standard (3-4 Star)", "Budget Hotel", "Hostel / Homestay"], index=1)
        with s_col2:
            transit_mode = st.selectbox("Transit Strategy", ["Express Flight", "Executive AC Train", "Overnight Bus", "Shared Shuttle"], index=1)
        with s_col3:
            dining_pref = st.selectbox("Culinary Mix", ["Gourmet Fine Dining", "Curated Local Bistros", "Street Food Trails"], index=1)

        # Calculate simulated savings
        hotel_mod = 1.4 if "5-Star" in hotel_tier else (0.8 if "3-4" in hotel_tier else 0.5)
        transit_mod = 1.3 if "Flight" in transit_mode else (0.7 if "Train" in transit_mode else 0.4)
        dining_mod = 1.5 if "Fine" in dining_pref else (0.9 if "Bistros" in dining_pref else 0.6)

        sim_hotel = costs.get("accommodation", 12000) * hotel_mod
        sim_transit = costs.get("transportation", 6000) * transit_mod
        sim_dining = costs.get("food", 5000) * dining_mod
        sim_total = sim_hotel + sim_transit + sim_dining + costs.get("activities", 3000) + costs.get("local_travel", 2000) + costs.get("miscellaneous", 1000)
        sim_rem = total_budget - sim_total

        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1rem; margin-top: 0.5rem; color: #F8FAFC;">
            <b>Simulated Rebalanced Spend:</b> <span style="font-size: 1.2rem; font-weight: 800; color: #34D399;">{currency_service.format_currency(sim_total, currency)}</span> &nbsp;|&nbsp; 
            <b>Simulated Balance:</b> <span style="font-weight: 700; color: {'#34D399' if sim_rem >= 0 else '#F87171'};">{currency_service.format_currency(sim_rem, currency)}</span>
        </div>
        """, unsafe_allow_html=True)

    # Plotly Charts Row
    st.write("")
    c_col1, c_col2 = st.columns(2)
    categories = ["Transportation", "Accommodation", "Food & Dining", "Activities", "Local Travel", "Buffer"]
    values = [
        costs.get("transportation", 0),
        costs.get("accommodation", 0),
        costs.get("food", 0),
        costs.get("activities", 0),
        costs.get("local_travel", 0),
        costs.get("miscellaneous", 0)
    ]

    with c_col1:
        fig_donut = px.pie(
            names=categories,
            values=values,
            hole=0.45,
            title=f"Category Distribution ({currency})",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c_col2:
        fig_bar = px.bar(
            x=categories,
            y=values,
            title=f"Expenditure by Category ({currency})",
            labels={"x": "Category", "y": f"Amount ({currency})"},
            color=values,
            color_continuous_scale="Tealgrn"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
