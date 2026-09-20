import streamlit as st
from datetime import date, timedelta
from config.constants import (
    CURRENCIES, TRAVEL_STYLES, INTERESTS,
    ACCOMMODATION_TYPES, FOOD_PREFERENCES, TRANSPORT_PREFERENCES
)
from services.geocoding_service import geocoding_service
from services.weather_service import weather_service
from services.ai_service import ai_service
from database.repositories import Repository
from database.models import create_trip_doc

def render_plan_trip_view():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 class="page-title">AI Trip Architect ✈️</h1>
        <p class="page-subtitle">
            Fill in your 9 travel preferences below. Our AI engine will harmonize your budget, dates, weather forecasts, and interests into a flawless itinerary.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check if prefilled destination from landing or explore page
    prefill_dest = st.session_state.get("prefill_destination", "")
    if prefill_dest:
        st.info(f"📍 Pre-selected Destination: **{prefill_dest}** (You can modify this to any global location)")

    with st.form("form_plan_trip"):
        # STEP 1: LOCATION
        st.markdown("### Step 1: Locations")
        c1, c2 = st.columns(2)
        with c1:
            start_location = st.text_input(
                "Starting Location / City",
                value="Hyderabad",
                help="Where will your journey begin?"
            ).strip()
        with c2:
            destination = st.text_input(
                "Destination (Accepts ANY Global Destination)",
                value=prefill_dest if prefill_dest else "Goa",
                help="Type any city, state, country or region e.g. Jaipur, Paris, Tokyo, Bali, Manali, London"
            ).strip()

        st.markdown("---")

        # STEP 2: DATES
        st.markdown("### Step 2: Travel Dates")
        d1, d2, d3 = st.columns([1, 1, 1])
        today = date.today()
        with d1:
            start_date = st.date_input("Start Date", value=today + timedelta(days=7), min_value=today)
        with d2:
            end_date = st.date_input("End Date", value=today + timedelta(days=11), min_value=today)
        
        # Calculate days
        if end_date < start_date:
            st.error("⚠️ End Date cannot be before Start Date.")
            days = 0
        else:
            days = (end_date - start_date).days + 1

        with d3:
            st.metric("Total Duration", f"{days} Days" if days > 0 else "Invalid", help="Calculated automatically from selected dates")

        st.markdown("---")

        # STEP 3: TRAVELERS & STEP 4: BUDGET
        st.markdown("### Steps 3 & 4: Travelers & Budget")
        b1, b2, b3 = st.columns(3)
        with b1:
            travelers = st.number_input("Number of Travelers", min_value=1, max_value=30, value=2, step=1)
        with b2:
            currency = st.selectbox("Currency", list(CURRENCIES.keys()), index=0)
        with b3:
            default_budget = 35000.0 if currency == "INR" else (500.0 if currency == "USD" else 450.0)
            budget = st.number_input(f"Total Budget ({currency})", min_value=50.0, value=default_budget, step=500.0)

        st.markdown("---")

        # STEP 5: TRAVEL STYLE & STEP 6: INTERESTS
        st.markdown("### Steps 5 & 6: Travel Style & Interests")
        s1, s2 = st.columns([1, 1.8])
        with s1:
            travel_style = st.selectbox("Travel Style", TRAVEL_STYLES, index=1)
        with s2:
            interests = st.multiselect(
                "Select Interests (Multiple Allowed)",
                INTERESTS,
                default=["Historical Places", "Nature", "Food"]
            )

        st.markdown("---")

        # STEP 7: ACCOMMODATION, STEP 8: FOOD, STEP 9: TRANSPORT
        st.markdown("### Steps 7, 8 & 9: Hospitality & Transit Preferences")
        p1, p2, p3 = st.columns(3)
        with p1:
            accommodation = st.selectbox("Accommodation Preference", ACCOMMODATION_TYPES, index=1)
        with p2:
            food_prefs = st.multiselect(
                "Food Preferences",
                FOOD_PREFERENCES,
                default=["Local Food", "Non-Vegetarian"]
            )
        with p3:
            transport_prefs = st.multiselect(
                "Transit Preferences",
                TRANSPORT_PREFERENCES,
                default=["Train", "Taxi"]
            )

        st.write("")
        st.markdown("""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; font-size: 0.9rem; color: #CBD5E1;">
            💡 <b>How it works:</b> Clicking below will geocode coordinates, query regional weather, balance your budget, invoke Gemini AI or resilient fallback models, and generate day-by-day morning/afternoon/evening schedules.
        </div>
        """, unsafe_allow_html=True)

        submit_plan = st.form_submit_button("✨ GENERATE MY AI TRIP", use_container_width=True, type="primary")

    # EXECUTION WORKFLOW
    if submit_plan:
        if not destination:
            st.error("Please provide a destination.")
            return
        if not start_location:
            st.error("Please provide your starting location.")
            return
        if days <= 0:
            st.error("Invalid travel dates. Please select an end date that is on or after the start date.")
            return
        if not interests:
            st.warning("Please select at least one interest to tailor your trip.")
            return

        with st.spinner("🚀 Analyzing destination, weather forecasts, and crafting your AI itinerary..."):
            # 1. Geocode
            dest_coords = geocoding_service.get_coordinates(destination)
            start_coords = geocoding_service.get_coordinates(start_location)

            # 2. Weather
            if dest_coords:
                weather_info = weather_service.get_weather(dest_coords[0], dest_coords[1], destination)
            else:
                weather_info = {
                    "is_live": False,
                    "location": destination,
                    "message": "Live weather unavailable.",
                    "advice": "General advice: Check regional weather advisories before travel."
                }

            # 3. AI / Fallback Recommendation Engine
            plan_result = ai_service.generate_trip_plan(
                start_location=start_location,
                destination=destination,
                start_date=str(start_date),
                end_date=str(end_date),
                days=days,
                travelers=int(travelers),
                budget=float(budget),
                currency=currency,
                travel_style=travel_style,
                interests=interests,
                accommodation_pref=accommodation,
                food_preferences=food_prefs if food_prefs else ["Local Food"],
                transport_preferences=transport_prefs if transport_prefs else ["Public Transport"],
                weather_info=weather_info
            )

            # Enrich result with coordinate and meta data
            plan_result["start_location"] = start_location
            plan_result["destination"] = destination
            plan_result["start_date"] = str(start_date)
            plan_result["end_date"] = str(end_date)
            plan_result["days"] = days
            plan_result["travelers"] = int(travelers)
            plan_result["budget"] = float(budget)
            plan_result["currency"] = currency
            plan_result["dest_coords"] = dest_coords
            plan_result["start_coords"] = start_coords
            plan_result["weather_info"] = weather_info

            # 4. Save to Database
            user = st.session_state.get("user") or {}
            user_id = user.get("_id", "guest_traveler")
            
            trip_doc = create_trip_doc(
                user_id=user_id,
                start_location=start_location,
                destination=destination,
                start_date=str(start_date),
                end_date=str(end_date),
                days=days,
                travelers=int(travelers),
                budget=float(budget),
                currency=currency,
                travel_style=travel_style,
                interests=interests,
                accommodation_pref=accommodation,
                food_prefs=food_prefs,
                transport_prefs=transport_prefs,
                itinerary=plan_result.get("itinerary", []),
                estimated_costs=plan_result.get("estimated_costs", {}),
                weather_info=weather_info,
                hotels=plan_result.get("hotels", []),
                restaurants=plan_result.get("restaurants", []),
                transport_options=plan_result.get("transport_options", []),
                travel_tips=plan_result.get("travel_tips", []),
                ai_mode="gemini" if plan_result.get("is_ai_mode") else "demo_fallback"
            )
            saved_id = Repository.save_trip(trip_doc)
            plan_result["_id"] = saved_id

            # Save in session state & redirect to Trip Results
            st.session_state.active_trip = plan_result
            st.session_state.current_page = "Trip Results"
            st.success("🎉 Trip successfully generated and saved to your database!")
            st.rerun()
