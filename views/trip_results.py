import streamlit as st
import plotly.express as px
import pandas as pd
from ui.components import render_kpi_card, render_demo_badge, render_ai_badge, render_section_header
from ui.maps import render_interactive_map
from services.currency_service import currency_service
from services.export_service import export_service
from database.repositories import Repository
from database.models import create_booking_doc

def render_trip_results_view():
    trip = st.session_state.get("active_trip")
    if not trip:
        st.warning("No active trip found. Please use the Trip Planner to create one.")
        if st.button("🚀 Go to Trip Planner"):
            st.session_state.current_page = "Plan My Trip"
            st.rerun()
        return

    dest = trip.get("destination", "Your Destination")
    curr = trip.get("currency", "INR")
    budget = trip.get("budget", 0)
    costs = trip.get("estimated_costs", {})
    total_cost = costs.get("total_estimated", 0)
    remaining = round(budget - total_cost, 2)
    is_over = remaining < 0

    # Header & AI Mode Badge
    st.markdown(f"""
    <div style="margin-bottom: 1.2rem;">
        <h1 class="page-title">Your AI-Powered Trip to {dest} 🗺️</h1>
        <p class="page-subtitle">Personalized itinerary, smart hospitality picks, routing, and budget optimization.</p>
    </div>
    """, unsafe_allow_html=True)

    if trip.get("is_ai_mode"):
        render_ai_badge("Generated with Google Gemini AI Architecture")
    else:
        render_demo_badge("AI service unavailable — using demo recommendation mode.")

    # KPI Summary Cards - Row 1
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    with row1_c1:
        render_kpi_card("Destination", dest, "Selected trip location")
    with row1_c2:
        render_kpi_card("Trip Duration", f"{trip.get('days', 1)} Days", f"{trip.get('start_date', '')} to {trip.get('end_date', '')}")
    with row1_c3:
        pax = trip.get('travelers', 1)
        render_kpi_card("Travelers", f"{pax} Person{'s' if pax > 1 else ''}", f"Style: {trip.get('travel_style', 'Standard')}")

    st.write("")
    # KPI Summary Cards - Row 2
    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        render_kpi_card("Total Budget", currency_service.format_currency(budget, curr), "Allocated travel budget")
    with row2_c2:
        render_kpi_card("Estimated Total Spend", currency_service.format_currency(total_cost, curr), "Stays, transit & activities")
    with row2_c3:
        rem_color = "#EF4444" if is_over else "#10B981"
        rem_text = f"<span style='color: {rem_color};'>{currency_service.format_currency(remaining, curr)}</span>"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Remaining Balance</div>
            <div class="kpi-value">{rem_text}</div>
            <div class="kpi-sub" style="color: {rem_color};">{'⚠️ Over Budget - Optimization Recommended' if is_over else '✓ Within Planned Budget'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Export & Action Bar
    with st.expander("📥 Download & Export Your Itinerary", expanded=False):
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            try:
                pdf_bytes = export_service.generate_pdf(trip)
                st.download_button(
                    label="📄 Download Trip PDF",
                    data=pdf_bytes,
                    file_name=f"Trip_to_{dest.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"PDF export note: {e}")
        with d_col2:
            csv_str = export_service.generate_csv(trip)
            st.download_button(
                label="📊 Export Schedule (CSV)",
                data=csv_str,
                file_name=f"Itinerary_{dest.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with d_col3:
            json_str = export_service.generate_json(trip)
            st.download_button(
                label="⚙️ Export Full Data (JSON)",
                data=json_str,
                file_name=f"Trip_{dest.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )

    # 10 Content Tabs for clean organization
    tab_itinerary, tab_stays, tab_dining, tab_transit, tab_weather, tab_budget, tab_map, tab_tips = st.tabs([
        "📅 Day-by-Day Itinerary",
        "🏨 Recommended Stays",
        "🍽️ Dining & Food",
        "🚗 Transit & Routes",
        "🌦️ Weather Intelligence",
        "💰 Budget & AI Optimizer",
        "🗺️ Interactive Map",
        "💡 Travel Tips & Summary"
    ])

    # 1. TAB: DAY-BY-DAY ITINERARY
    with tab_itinerary:
        render_section_header(f"Curated Timeline for {dest}", "Morning, Afternoon, and Evening activities planned with logical pacing")
        itinerary = trip.get("itinerary", [])
        if not itinerary:
            st.info("No timeline items generated.")
        for day in itinerary:
            d_num = day.get("day", 1)
            d_date = day.get("date", "")
            d_theme = day.get("theme", "")
            
            st.markdown(f"""
            <div class="timeline-day">
                <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">
                    Day {d_num} &nbsp;•&nbsp; <span style="font-size: 0.95rem; color: #94A3B8;">{d_date}</span> &nbsp;•&nbsp; 
                    <span style="color: #2DD4BF;">{d_theme}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            m_col, a_col, e_col = st.columns(3)
            # Morning
            with m_col:
                m = day.get("morning", {})
                st.markdown(f"""
                <div class="timeline-period">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #FB923C; text-transform: uppercase;">🌅 Morning ({m.get('time', '9:00 AM')})</div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC; margin-top: 0.25rem;">{m.get('activity')}</div>
                    <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem;">📍 {m.get('location')} &nbsp;|&nbsp; ⏱️ {m.get('duration')}</div>
                    <div style="font-size: 0.8rem; color: #2DD4BF; margin-top: 0.4rem;">☕ {m.get('meal_recommendation')}</div>
                </div>
                """, unsafe_allow_html=True)
            # Afternoon
            with a_col:
                a = day.get("afternoon", {})
                st.markdown(f"""
                <div class="timeline-period">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #38BDF8; text-transform: uppercase;">☀️ Afternoon ({a.get('time', '1:30 PM')})</div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC; margin-top: 0.25rem;">{a.get('activity')}</div>
                    <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem;">📍 {a.get('location')} &nbsp;|&nbsp; ⏱️ {a.get('duration')}</div>
                    <div style="font-size: 0.8rem; color: #2DD4BF; margin-top: 0.4rem;">🍽️ {a.get('meal_recommendation')}</div>
                </div>
                """, unsafe_allow_html=True)
            # Evening
            with e_col:
                e = day.get("evening", {})
                st.markdown(f"""
                <div class="timeline-period">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #A78BFA; text-transform: uppercase;">🌙 Evening ({e.get('time', '6:00 PM')})</div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC; margin-top: 0.25rem;">{e.get('activity')}</div>
                    <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem;">📍 {e.get('location')} &nbsp;|&nbsp; ⏱️ {e.get('duration')}</div>
                    <div style="font-size: 0.8rem; color: #2DD4BF; margin-top: 0.4rem;">🍷 {e.get('meal_recommendation')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

    # 2. TAB: RECOMMENDED STAYS & BOOKING WORKFLOW
    with tab_stays:
        render_section_header("🏨 Accommodations Matching Your Style", "Carefully vetted properties with estimated pricing")
        hotels = trip.get("hotels", [])
        if not hotels:
            st.info("No hotels returned.")
        for h in hotels:
            with st.container():
                h_col1, h_col2 = st.columns([1, 2])
                with h_col1:
                    img_url = h.get("image_url", "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80")
                    st.image(img_url, use_container_width=True)
                with h_col2:
                    st.markdown(f"### {h.get('name')}")
                    st.markdown(f"⭐ **{h.get('star_rating', 4)}-Star Property** &nbsp;|&nbsp; Guest Rating: **{h.get('guest_rating', 4.8)}/5.0**")
                    st.markdown(f"📍 *{h.get('address', dest)}*")
                    st.write(h.get("description", ""))
                    st.markdown(f"**Amenities:** {', '.join(h.get('amenities', []))}")
                    
                    price_night = h.get("price_per_night_converted", h.get("price_per_night", 4000))
                    total_h_price = h.get("total_estimated_price", price_night * trip.get("days", 1))
                    st.markdown(f"**Price per Night:** {currency_service.format_currency(price_night, curr)} &nbsp;|&nbsp; **Estimated Total ({trip.get('days', 1)} nights):** <span style='font-size: 1.2rem; font-weight: 800; color: #F97316;'>{currency_service.format_currency(total_h_price, curr)}</span>", unsafe_allow_html=True)
                    
                    b_btn1, b_btn2 = st.columns(2)
                    with b_btn1:
                        # Request Booking Workflow
                        if st.button(f"🛎️ Request Booking: {h.get('name')[:18]}...", key=f"req_book_{h.get('_id', h.get('name'))}", type="primary"):
                            user = st.session_state.get("user") or {}
                            user_id = user.get("_id", "guest_traveler")
                            bkg_doc = create_booking_doc(
                                user_id=user_id,
                                user_name=user.get("full_name", "Traveler"),
                                user_email=user.get("email", "guest@example.com"),
                                provider_id=h.get("provider_id", "system"),
                                listing_id=h.get("_id", "htl_001"),
                                listing_type="Hotel",
                                listing_name=h.get("name"),
                                trip_id=trip.get("_id", ""),
                                dates=f"{trip.get('start_date')} to {trip.get('end_date')}",
                                guests=trip.get("travelers", 1),
                                total_price=float(total_h_price),
                                currency=curr,
                                status="Pending"
                            )
                            bkg_id = Repository.create_booking(bkg_doc)
                            st.success(f"🎉 Booking Request submitted (ID: {bkg_id}). Status is currently **Pending**. The provider will review and confirm.")
                    with b_btn2:
                        # Save to Favorites
                        user = st.session_state.get("user") or {}
                        user_id = user.get("_id", "guest_traveler")
                        if st.button(f"❤️ Save to Favorites", key=f"fav_{h.get('_id', h.get('name'))}"):
                            is_fav = Repository.toggle_favorite(
                                user_id=user_id,
                                item_id=h.get("_id", h.get("name")),
                                item_type="hotel",
                                title=h.get("name"),
                                image_url=h.get("image_url", ""),
                                destination=dest,
                                price_info=f"{currency_service.format_currency(price_night, curr)}/night"
                            )
                            if is_fav:
                                st.success("Saved to your Favorites!")
                            else:
                                st.info("Removed from Favorites.")
                st.markdown("---")

    # 3. TAB: DINING & RESTAURANTS
    with tab_dining:
        render_section_header("🍽️ Handpicked Dining & Street Trails", "Top eateries based on your dietary preferences")
        rests = trip.get("restaurants", [])
        r_cols = st.columns(3)
        for idx, r in enumerate(rests):
            with r_cols[idx % 3]:
                st.markdown(f"""
                <div class="travel-card">
                    <img src="{r.get('image_url', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=500&q=80')}">
                    <div class="travel-card-body">
                        <span style="font-size: 0.75rem; color: #2DD4BF; font-weight: 700;">{r.get('cuisine', 'Cuisine')} • {r.get('price_level', '$$')}</span>
                        <div class="travel-card-title">{r.get('name')}</div>
                        <div class="travel-card-subtitle">📍 {r.get('address', dest)}</div>
                        <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 0.5rem;">{r.get('description', '')}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                            <span style="font-size: 0.85rem; color: #94A3B8;">Avg: <b style="color: #F8FAFC;">{currency_service.format_currency(r.get('avg_cost_converted', 600), curr)}</b></span>
                            <span class="travel-card-price">★ {r.get('rating', 4.6)}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                user = st.session_state.get("user") or {}
                user_id = user.get("_id", "guest_traveler")
                if st.button(f"Bookmark {r.get('name')[:14]}", key=f"btn_fav_rest_{idx}"):
                    Repository.toggle_favorite(
                        user_id=user_id,
                        item_id=r.get("_id", r.get("name")),
                        item_type="restaurant",
                        title=r.get("name"),
                        image_url=r.get("image_url", ""),
                        destination=dest,
                        price_info=f"Avg {currency_service.format_currency(r.get('avg_cost_converted', 600), curr)}"
                    )
                    st.success("Restaurant bookmarked!")

    # 4. TAB: TRANSPORTATION & TRANSIT
    with tab_transit:
        render_section_header(f"🚗 Journey Options: {trip.get('start_location')} ➔ {dest}", "Multi-modal route estimates and local city travel guidance")
        trans_options = trip.get("transport_options", [])
        for t in trans_options:
            cost_converted = t.get("total_cost_converted", t.get("cost", 3000))
            st.markdown(f"""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="color: #38BDF8; margin: 0;">🚀 {t.get('type')}</h4>
                    <span style="font-size: 1.25rem; font-weight: 800; color: #FB923C;">{currency_service.format_currency(cost_converted, curr)} (Group Total)</span>
                </div>
                <p style="color: #CBD5E1; margin-top: 0.3rem; margin-bottom: 0.5rem;">
                    <b>Duration:</b> {t.get('duration')} &nbsp;|&nbsp; 
                    <b>Convenience:</b> {t.get('convenience', 'High')} &nbsp;|&nbsp; 
                    <b>Carrier / Vehicle:</b> {t.get('vehicle_details', 'Standard Commercial')}
                </p>
                <div style="font-size: 0.85rem; color: #94A3B8;">{t.get('description')}</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.3rem;">ℹ️ {t.get('availability_note', 'Estimated market fares')}</div>
            </div>
            """, unsafe_allow_html=True)

    # 5. TAB: WEATHER INTELLIGENCE
    with tab_weather:
        render_section_header(f"🌦️ Weather Forecast: {dest}", "Live conditions and weather-adaptive travel scheduling")
        winfo = trip.get("weather_info", {})
        if winfo.get("is_live"):
            wc1, wc2, wc3, wc4 = st.columns(4)
            with wc1:
                render_kpi_card("Current Temp", f"{winfo.get('temperature', '--')} °C", winfo.get("condition", ""))
            with wc2:
                render_kpi_card("Humidity", f"{winfo.get('humidity', '--')} %", "Relative air humidity")
            with wc3:
                render_kpi_card("Wind Speed", f"{winfo.get('wind_speed', '--')} km/h", "Surface winds")
            with wc4:
                render_kpi_card("Sun Schedule", f"🌅 {winfo.get('sunrise', '--')}", f"🌇 Sunset {winfo.get('sunset', '--')}")
            
            st.write("")
            st.markdown(f"""
            <div style="background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 1rem 1.25rem; border-radius: 0 12px 12px 0;">
                <b style="color: #1E40AF;">🤖 Gemini Weather Advice:</b>
                <p style="color: #1E3A8A; margin-top: 0.25rem; margin-bottom: 0;">{winfo.get('advice')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Forecast table
            forecast = winfo.get("forecast", [])
            if forecast:
                st.write("")
                st.markdown("##### 7-Day Regional Trend")
                df_weather = pd.DataFrame(forecast)
                st.dataframe(df_weather, use_container_width=True)
        else:
            render_demo_badge("Weather information unavailable in demo mode.")
            st.info(winfo.get("advice", "Pack comfortable attire suited to typical regional climate."))

    # 6. TAB: BUDGET & AI OPTIMIZER
    with tab_budget:
        render_section_header("💰 Budget Dashboard & AI Optimizer", "Comprehensive expense breakdown and instant cost-saving substitutions")
        
        # Plotly Donut Chart
        cat_labels = ["Transportation", "Accommodation", "Food & Dining", "Activities", "Local Travel", "Buffer"]
        cat_values = [
            costs.get("transportation", 0),
            costs.get("accommodation", 0),
            costs.get("food", 0),
            costs.get("activities", 0),
            costs.get("local_travel", 0),
            costs.get("miscellaneous", 0)
        ]
        
        b_chart_col1, b_chart_col2 = st.columns([1, 1])
        with b_chart_col1:
            fig_donut = px.pie(
                values=cat_values,
                names=cat_labels,
                hole=0.5,
                title=f"Cost Allocation ({curr})",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_donut.update_layout(margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_donut, use_container_width=True)

        with b_chart_col2:
            fig_bar = px.bar(
                x=["Total Budget", "Estimated Cost"],
                y=[budget, total_cost],
                color=["Total Budget", "Estimated Cost"],
                color_discrete_map={"Total Budget": "#0D9488", "Estimated Cost": "#F97316" if not is_over else "#DC2626"},
                title=f"Budget vs. Estimated Spend ({curr})"
            )
            fig_bar.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_bar, use_container_width=True)

        # AI Budget Optimizer Alerts & Alternatives
        analysis = trip.get("budget_analysis", {})
        if is_over or analysis.get("is_over_budget"):
            st.warning(f"⚠️ **Budget Alert:** Your estimated expenses exceed your allocated budget by **{currency_service.format_currency(abs(remaining), curr)}**.")
            st.markdown("#### 💡 AI Smart Budget Substitutions:")
            alts = analysis.get("alternatives", [])
            for alt in alts:
                st.markdown(f"""
                <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
                    <b style="color: #92400E;">{alt.get('category')} Optimization:</b><br>
                    <span style="color: #78350F;">From: <s>{alt.get('original')}</s> ➔ <b>{alt.get('suggestion')}</b></span><br>
                    <span style="color: #059669; font-weight: 700; font-size: 0.85rem;">Potential Savings: ~{alt.get('potential_savings')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(f"✓ **Budget On Track!** You have an estimated buffer of **{currency_service.format_currency(remaining, curr)}** for extra leisure or shopping.")

    # 7. TAB: INTERACTIVE MAP
    with tab_map:
        render_section_header(f"🗺️ Visual Map of {dest}", "Interactive pins showing your origin, destination, hotels, dining, and attractions")
        render_interactive_map(
            destination_coords=trip.get("dest_coords"),
            start_coords=trip.get("start_coords"),
            destination_name=dest,
            hotels=trip.get("hotels"),
            restaurants=trip.get("restaurants"),
            attractions=trip.get("attractions")
        )

    # 8. TAB: TRAVEL TIPS & SUMMARY
    with tab_tips:
        render_section_header("💡 Destination Intelligence & Tips", "Crucial guidelines, etiquette, and logistics")
        if trip.get("destination_summary"):
            st.markdown(f"**Overview:** {trip['destination_summary']}")
        
        tips = trip.get("travel_tips", [])
        for t in tips:
            st.markdown(f"- {t}")
