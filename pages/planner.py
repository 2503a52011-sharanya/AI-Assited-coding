import streamlit as st
from datetime import date, timedelta
import plotly.express as px

from config.settings import (
    TRAVELER_TYPES, TRAVEL_STYLES, TRANSPORT_TYPES,
    ACCOMMODATION_TYPES, FOOD_PREFERENCES, INTEREST_CATEGORIES
)
from services.destination_service import DestinationService
from services.weather_service import WeatherService
from services.flight_service import FlightService
from services.train_service import TrainService
from services.bus_service import BusService
from services.hotel_service import HotelService
from services.activity_service import ActivityService
from services.itinerary_service import ItineraryService
from services.budget_service import BudgetService
from services.map_service import MapService
from services.booking_service import BookingService
from database.queries import save_trip, save_itinerary, save_budget
from utils.helpers import format_currency


def render_planner_page():
    # Page Heading
    st.markdown("# ✈️ Plan Your Perfect Trip")
    st.markdown("<p style='color: #475569; font-size: 1.05rem; margin-top: -8px; margin-bottom: 20px;'>Create a personalized trip based on your destination, interests, travel style and budget.</p>", unsafe_allow_html=True)
    st.markdown("### 📋 Trip Configuration & Preferences")

    # Preload destination name and traveler type from session if available
    prefilled_dest = st.session_state.get("selected_destination_name", "Araku Valley")
    prefilled_origin = st.session_state.get("selected_origin", "Hyderabad")
    
    # Synchronize incoming traveler type if passed from another view
    if "selected_traveler_type" in st.session_state:
        raw_tt = st.session_state.get("selected_traveler_type")
        if raw_tt in TRAVELER_TYPES:
            st.session_state["plan_traveler_type"] = raw_tt
            st.session_state["plan_travelers"] = 1 if raw_tt == "Solo" else (2 if raw_tt == "Couple" else (4 if raw_tt in ["Family", "Friends"] else 6))
        elif raw_tt == "All Travelers":
            if "plan_traveler_type" not in st.session_state:
                st.session_state["plan_traveler_type"] = "Solo"
                st.session_state["plan_travelers"] = 1

    # Ensure widget defaults in session state
    if "plan_traveler_type" not in st.session_state:
        st.session_state["plan_traveler_type"] = "Solo"
    if "plan_travelers" not in st.session_state:
        st.session_state["plan_travelers"] = 1 if st.session_state["plan_traveler_type"] == "Solo" else (2 if st.session_state["plan_traveler_type"] == "Couple" else 4)

    def on_traveler_type_change():
        chosen_tt = st.session_state.get("plan_traveler_type")
        if chosen_tt == "Solo":
            st.session_state["plan_travelers"] = 1
        elif chosen_tt == "Couple":
            st.session_state["plan_travelers"] = 2
        elif chosen_tt in ["Family", "Friends"]:
            st.session_state["plan_travelers"] = 4
        elif chosen_tt in ["Group", "Business"]:
            st.session_state["plan_travelers"] = 6 if chosen_tt == "Group" else 1
        st.session_state.pop("plan_generated", None)

    def on_travelers_count_change():
        cnt = st.session_state.get("plan_travelers", 1)
        if cnt == 1:
            st.session_state["plan_traveler_type"] = "Solo"
        elif cnt == 2:
            st.session_state["plan_traveler_type"] = "Couple"
        elif cnt in [3, 4]:
            if st.session_state.get("plan_traveler_type") not in ["Family", "Friends"]:
                st.session_state["plan_traveler_type"] = "Family"
        elif cnt >= 5:
            st.session_state["plan_traveler_type"] = "Group"
        st.session_state.pop("plan_generated", None)

    # Step 1: User Input Form with Clean Cards
    with st.container(border=True):
        # Section 1: Trip Details Card
        st.markdown("##### 📍 Trip Details")
        c1_1, c1_2 = st.columns(2)
        with c1_1:
            origin = st.text_input("Starting Location", value=prefilled_origin, key="plan_origin")
            start_date = st.date_input("Travel Date", value=date.today() + timedelta(days=7), key="plan_start_date")
        with c1_2:
            destination_input = st.text_input("Destination", value=prefilled_dest, key="plan_dest")
            days_count = st.number_input("Number of Days", min_value=1, max_value=14, value=3, step=1, key="plan_days")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Section 2: Budget & Travelers Card
        st.markdown("##### 💰 Budget & Travel Style")
        c2_1, c2_2 = st.columns(2)
        with c2_1:
            target_budget = st.number_input("Total Trip Budget (₹)", min_value=2000, max_value=500000, value=20000, step=1000, key="plan_budget")
            travelers_count = st.number_input("Number of Travelers", min_value=1, max_value=20, step=1, key="plan_travelers", on_change=on_travelers_count_change)
        with c2_2:
            travel_style = st.selectbox("Travel Style", TRAVEL_STYLES, index=2, key="plan_travel_style")
            curr_tt = st.session_state.get("plan_traveler_type", "Solo")
            tt_idx = TRAVELER_TYPES.index(curr_tt) if curr_tt in TRAVELER_TYPES else 0
            traveler_type = st.selectbox("Traveler Type", TRAVELER_TYPES, index=tt_idx, key="plan_traveler_type", on_change=on_traveler_type_change)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Section 3: Preferences Card
        st.markdown("##### ⚙️ Travel Preferences")
        c3_1, c3_2 = st.columns(2)
        with c3_1:
            transport_pref = st.selectbox("Transportation", ["Train", "Bus", "Flight", "Cab", "Train + Local Cab"], index=0, key="plan_transport")
            food_pref = st.selectbox("Food Preference", FOOD_PREFERENCES, index=0, key="plan_food")
        with c3_2:
            accommodation_pref = st.selectbox("Accommodation", ACCOMMODATION_TYPES, index=1, key="plan_hotel_type")
            interests = st.multiselect(
                "Interests",
                INTEREST_CATEGORIES,
                default=["Nature", "Photography"],
                key="plan_interests"
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        generate_clicked = st.button("✨ Generate My Personalized Trip", type="primary", width="stretch")

    # Process Generation
    if generate_clicked or st.session_state.get("plan_generated"):
        st.session_state["plan_generated"] = True
        
        # 1. Resolve Destination
        with st.spinner(f"Resolving destination information for '{destination_input}'..."):
            dest_obj = DestinationService.get_by_name_or_discover(destination_input)
            if not dest_obj:
                st.error("Could not resolve this location. Please try another name.")
                return

        dest_id = dest_obj["id"]
        dest_name = dest_obj["name"]
        dest_lat = float(dest_obj["latitude"])
        dest_lon = float(dest_obj["longitude"])

        # 2. Weather Advisory
        weather_info = WeatherService.get_weather(dest_lat, dest_lon, dest_name)
        advisories = WeatherService.get_itinerary_weather_advisory(weather_info)

        # 3. Retrieve Options
        details = DestinationService.get_details(dest_id)
        attractions = details["attractions"]
        activities = details["activities"]
        hotels = details["hotels"]

        # 4. Resolve Transport Pricing
        transport_fare_person = 480.0 # default train
        selected_provider = "IRCTC Railway / State Bus"
        if "Flight" in transport_pref:
            flights = FlightService.search_flights(origin, dest_name, str(start_date))
            if flights:
                transport_fare_person = flights[0]["price_economy"]
                selected_provider = flights[0]["provider"]
        elif "Bus" in transport_pref:
            buses = BusService.search_buses(origin, dest_name, str(start_date))
            if buses:
                transport_fare_person = buses[0]["fare"]
                selected_provider = buses[0]["operator"]
        elif "Cab" in transport_pref and "Train" not in transport_pref:
            transport_fare_person = 3500.0
            selected_provider = "Outstation Tourist Cab"
        else: # Train or Train + Local Cab
            trains = TrainService.search_trains(origin, dest_name, str(start_date))
            if trains:
                transport_fare_person = trains[0]["fare_sleeper"] if travel_style == "Budget" else trains[0]["fare_3ac"]
                selected_provider = trains[0]["train_name"]

        # 5. Resolve Hotel Pricing
        hotel_nightly = 1500.0
        selected_hotel_name = "Valley View Residency"
        if hotels:
            # Pick matching or lowest budget
            selected_hotel = hotels[0]
            for h in hotels:
                if accommodation_pref.lower() in h["hotel_type"].lower():
                    selected_hotel = h
                    break
            hotel_nightly = float(selected_hotel["price_per_night"])
            selected_hotel_name = selected_hotel["name"]

        # 6. Activities Cost
        total_act_fee = sum(float(a.get("entry_fee", 0.0)) for a in attractions[:4])

        # 7. Calculate Budget
        budget_calc = BudgetService.calculate_trip_budget(
            days=days_count,
            travelers=travelers_count,
            transport_fare_per_person=transport_fare_person,
            hotel_nightly_rate=hotel_nightly,
            food_style=food_pref,
            travel_style=travel_style,
            activities_cost_per_person=total_act_fee,
            local_cab_daily_rate=1400.0 if "Local Cab" in transport_pref else 800.0
        )

        # 8. Budget Optimization Check
        optimization_result = BudgetService.optimize_budget(
            user_budget=target_budget,
            original_plan=budget_calc,
            days=days_count,
            travelers=travelers_count,
            current_transport_type=transport_pref,
            current_hotel_price=hotel_nightly
        )

        # Active plan is optimized if needed
        active_plan = optimization_result["optimized_plan"] if optimization_result["needs_optimization"] else budget_calc

        # 9. Generate Day-by-Day Schedule
        itinerary = ItineraryService.generate_itinerary(
            destination_name=dest_name,
            days=days_count,
            traveler_type=traveler_type,
            interests=interests,
            attractions=attractions,
            activities=activities,
            hotel_name=selected_hotel_name,
            weather_advisory=advisories
        )

        # -------------------------------------------------------------
        # DISPLAY SECTION
        # -------------------------------------------------------------
        st.markdown("---")
        st.header(f"✨ Custom Travel Plan: {origin} ➔ {dest_name}")
        st.markdown(f"**👥 Confirmed Group Setup:** `{travelers_count} Traveler(s)` | **Type:** `{traveler_type}` | **Style:** `{travel_style}` | **Budget:** `{format_currency(target_budget)}`")
        
        # Weather Banner
        wcol1, wcol2, wcol3 = st.columns([1, 1, 2])
        with wcol1:
            st.metric("Current Weather", f"{weather_info['temperature']}°C", weather_info['condition'])
        with wcol2:
            st.metric("Rain Chance", f"{weather_info.get('forecast', [{}])[0].get('rain_probability', 10)}%")
        with wcol3:
            if advisories:
                for adv in advisories:
                    st.info(adv)
            else:
                st.success("🌤️ Ideal weather forecast for outdoor touring and sightseeing.")

        # Tabbed Plan Details
        tab_itinerary, tab_budget, tab_map, tab_book = st.tabs([
            "📅 Day-by-Day Itinerary", "💰 Budget & Optimization", "🗺️ Interactive Map", "💳 Book Complete Trip"
        ])

        # TAB 1: ITINERARY
        with tab_itinerary:
            st.subheader(f"Detailed Schedule for {days_count} Days — {traveler_type} Journey")
            for day_idx in range(1, days_count + 1):
                day_items = [i for i in itinerary if i["day"] == day_idx]
                with st.expander(f"📍 Day {day_idx} Schedule", expanded=True):
                    for item in day_items:
                        icol1, icol2, icol3 = st.columns([1.5, 3.5, 1])
                        with icol1:
                            st.markdown(f"**⏰ {item['time_slot']}**")
                            st.caption(f"`{item['activity_type']}`")
                        with icol2:
                            st.markdown(f"**{item['activity_title']}**")
                            st.write(item.get("notes", ""))
                        with icol3:
                            cost = item.get("estimated_cost", 0.0)
                            st.markdown(f"*{format_currency(cost)}*" if cost > 0 else "*Included*")
                        st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

        # TAB 2: BUDGET & OPTIMIZATION
        with tab_budget:
            st.subheader("Financial Summary & Cost Optimization")

            b_met1, b_met2, b_met3, b_met4 = st.columns(4)
            with b_met1:
                st.metric("Your Budget", format_currency(target_budget))
            with b_met2:
                st.metric("Estimated Cost", format_currency(active_plan["total_estimated_cost"]))
            with b_met3:
                rem = target_budget - active_plan["total_estimated_cost"]
                st.metric("Remaining Balance", format_currency(rem), delta=f"{format_currency(rem)}")
            with b_met4:
                st.metric("Cost Per Person", format_currency(active_plan["cost_per_person"]))

            # Optimization Banner if triggered
            if optimization_result["needs_optimization"]:
                st.warning(f"⚡ **Smart Budget Optimization Applied!** The initial plan ({format_currency(optimization_result['original_plan']['total_estimated_cost'])}) exceeded your budget. We optimized it to **{format_currency(optimization_result['optimized_plan']['total_estimated_cost'])}**, saving you **{format_currency(optimization_result['savings'])}**!")
                
                # Comparison Table
                comp_col1, comp_col2 = st.columns(2)
                with comp_col1:
                    st.markdown("#### ❌ Original Unoptimized Plan")
                    st.write(f"- Transportation: {format_currency(optimization_result['original_plan']['transport_cost'])}")
                    st.write(f"- Accommodation: {format_currency(optimization_result['original_plan']['accommodation_cost'])}")
                    st.write(f"- Dining & Food: {format_currency(optimization_result['original_plan']['food_cost'])}")
                    st.write(f"- Sightseeing & Activities: {format_currency(optimization_result['original_plan']['activities_cost'])}")
                    st.write(f"- Local Transit: {format_currency(optimization_result['original_plan']['local_transport_cost'])}")
                    st.markdown(f"**Total: {format_currency(optimization_result['original_plan']['total_estimated_cost'])}**")
                with comp_col2:
                    st.markdown("#### ✅ Smart Optimized Plan")
                    st.write(f"- Transportation: {format_currency(optimization_result['optimized_plan']['transport_cost'])}")
                    st.write(f"- Accommodation: {format_currency(optimization_result['optimized_plan']['accommodation_cost'])}")
                    st.write(f"- Dining & Food: {format_currency(optimization_result['optimized_plan']['food_cost'])}")
                    st.write(f"- Sightseeing & Activities: {format_currency(optimization_result['optimized_plan']['activities_cost'])}")
                    st.write(f"- Local Transit: {format_currency(optimization_result['optimized_plan']['local_transport_cost'])}")
                    st.markdown(f"**Total: {format_currency(optimization_result['optimized_plan']['total_estimated_cost'])}**")

                st.markdown("##### 💡 Adjustments Made:")
                for rec in optimization_result["recommendations"]:
                    st.markdown(f"- {rec}")

            # Plotly Donut Breakdown
            fig = px.pie(
                values=list(active_plan["breakdown_percentages"].values()),
                names=list(active_plan["breakdown_percentages"].keys()),
                title="Expense Category Distribution",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            st.plotly_chart(fig, width="stretch")

        # TAB 3: MAP
        with tab_map:
            st.subheader(f"Route & Points of Interest: {dest_name}")
            map_df = MapService.generate_map_dataframe(dest_name, dest_lat, dest_lon, attractions)
            st.map(map_df, latitude="latitude", longitude="longitude", size="size")
            st.caption(f"Coordinates: {dest_lat:.4f}° N, {dest_lon:.4f}° E | State: {dest_obj['state']}")

        # TAB 4: BOOK COMPLETE TRIP
        with tab_book:
            st.subheader("One-Click Comprehensive Booking")
            st.caption("Reserve your verified travel transportation and accommodation directly from this screen.")

            user_id = st.session_state.get("user_id", 2)
            end_date = start_date + timedelta(days=days_count)

            st.markdown(f"""
            **Booking Package Overview:**
            - **Transport:** {selected_provider} ({origin} ➔ {dest_name})
            - **Accommodation:** {selected_hotel_name} ({days_count - 1} nights, {max(1, travelers_count // 2)} room(s))
            - **Travelers:** {travelers_count} person(s)
            - **Dates:** {start_date} to {end_date}
            - **Total Package Payable:** **{format_currency(active_plan['total_estimated_cost'])}**
            """)

            # Passenger Inputs
            st.markdown("##### Lead Passenger Details")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                p_name = st.text_input("Lead Traveler Name", value=st.session_state.get("user_name", "Rohit Sharma"), key="lead_p_name")
            with p_col2:
                p_age = st.number_input("Age", min_value=5, max_value=100, value=28, key="lead_p_age")

            payment_mode = st.radio("Select Payment Method", ["UPI / QR Code (Demo)", "Net Banking", "Credit / Debit Card"], horizontal=True)

            if st.button("💳 Confirm & Book Package", type="primary", width="stretch"):
                # 1. Save Trip
                trip_id = save_trip(
                    user_id=user_id,
                    trip_name=f"Trip to {dest_name} ({days_count}D/{traveler_type})",
                    origin=origin,
                    destination=dest_name,
                    start_date=start_date,
                    end_date=end_date,
                    days=days_count,
                    travelers_count=travelers_count,
                    traveler_type=traveler_type,
                    travel_style=travel_style,
                    allocated_budget=target_budget,
                    total_estimated_cost=active_plan["total_estimated_cost"]
                )

                # 2. Save Itinerary
                save_itinerary(trip_id, itinerary)

                # 3. Save Budget
                save_budget(
                    trip_id=trip_id,
                    transport_cost=active_plan["transport_cost"],
                    accommodation_cost=active_plan["accommodation_cost"],
                    food_cost=active_plan["food_cost"],
                    activities_cost=active_plan["activities_cost"],
                    local_transport_cost=active_plan["local_transport_cost"],
                    buffer_cost=active_plan["buffer_cost"],
                    total_cost=active_plan["total_estimated_cost"],
                    is_optimized=optimization_result["needs_optimization"],
                    savings=optimization_result["savings"]
                )

                # 4. Create Transport Booking
                passengers = [{"name": p_name, "age": p_age, "seat": "Confirmed"}]
                trans_bk = BookingService.book_ticket(
                    user_id=user_id,
                    category="Train" if "Train" in transport_pref else "Bus",
                    provider_name=selected_provider,
                    item_title=f"{origin} to {dest_name}",
                    travel_date=str(start_date),
                    passenger_count=travelers_count,
                    total_amount=active_plan["transport_cost"],
                    passengers=passengers,
                    trip_id=trip_id,
                    payment_method=payment_mode
                )

                # 5. Create Hotel Booking
                hotel_bk = BookingService.book_ticket(
                    user_id=user_id,
                    category="Hotel",
                    provider_name=selected_hotel_name,
                    item_title=f"{selected_hotel_name} ({days_count - 1} Nights)",
                    travel_date=str(start_date),
                    passenger_count=travelers_count,
                    total_amount=active_plan["accommodation_cost"],
                    passengers=passengers,
                    trip_id=trip_id,
                    payment_method=payment_mode
                )

                st.success(f"🎉 **Trip & Bookings Confirmed!** Saved to your profile. (Transport Ref: `{trans_bk['booking_reference']}`, Hotel Ref: `{hotel_bk['booking_reference']}`)")
                st.balloons()
                
                # Navigate to My Trips or My Bookings
                btn_goto_trips, btn_goto_bookings = st.columns(2)
                with btn_goto_trips:
                    if st.button("View in 'My Trips'", key="goto_trips"):
                        st.switch_page("pages/trips.py")
                with btn_goto_bookings:
                    if st.button("View in 'My Bookings'", key="goto_bookings"):
                        st.switch_page("pages/bookings.py")


render_planner_page()

