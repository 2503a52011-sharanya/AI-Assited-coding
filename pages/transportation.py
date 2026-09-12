import streamlit as st
from datetime import date, timedelta
from services.flight_service import FlightService
from services.train_service import TrainService
from services.bus_service import BusService
from services.booking_service import BookingService
from utils.helpers import format_currency


def render_transportation_page():
    st.title("🚆 Transportation Hub")
    st.caption("Search, compare, and instantly book Flights, Trains, Buses, and Cabs across India.")

    # Search Box
    scol1, scol2, scol3, scol4 = st.columns([2, 2, 1.5, 1.5])
    with scol1:
        origin = st.text_input("Origin City", value=st.session_state.get("selected_origin", "Hyderabad"), key="t_origin")
    with scol2:
        dest = st.text_input("Destination City", value=st.session_state.get("selected_destination_name", "Araku Valley"), key="t_dest")
    with scol3:
        travel_date = st.date_input("Date of Travel", value=date.today() + timedelta(days=5), key="t_date")
    with scol4:
        sort_by = st.selectbox("Sort By", ["Cheapest", "Fastest", "Best Value"], key="t_sort")

    # Tabs for transport modes
    t_tab_train, t_tab_bus, t_tab_flight, t_tab_cab = st.tabs([
        "🚂 Trains (IRCTC)", "🚌 Buses", "✈️ Flights", "🚖 Outstation Cabs"
    ])

    user_id = st.session_state.get("user_id", 2)

    # 1. TRAINS
    with t_tab_train:
        trains = TrainService.search_trains(origin, dest, str(travel_date), sort_by=sort_by)
        st.subheader(f"Available Trains ({len(trains)})")
        if trains:
            for t in trains:
                with st.container(border=True):
                    tcol1, tcol2, tcol3, tcol4 = st.columns([3, 2, 2, 1.5])
                    with tcol1:
                        st.markdown(f"### {t['train_name']}")
                        st.caption(f"Train #{t['train_number']} | Classes: {', '.join(t['classes'])}")
                    with tcol2:
                        st.markdown(f"**Depart:** {t['departure']} ➔ **Arrive:** {t['arrival']}")
                        st.markdown(f"⏱️ Duration: `{t['duration_str']}`")
                    with tcol3:
                        st.markdown(f"Sleeper: **{format_currency(t['fare_sleeper'])}**")
                        st.markdown(f"3AC: **{format_currency(t['fare_3ac'])}**")
                        st.caption(f"Seats: {t['available_seats']} Available")
                    with tcol4:
                        if st.button("Book Train", key=f"bk_trn_{t['id']}", type="primary", width="stretch"):
                            st.session_state["active_booking_item"] = {
                                "category": "Train",
                                "provider": t["train_name"],
                                "title": f"Train #{t['train_number']} ({origin} to {dest})",
                                "amount": t["fare_3ac"],
                                "date": str(travel_date)
                            }
                            st.rerun()
        else:
            st.info("No direct trains found for this route.")

    # 2. BUSES
    with t_tab_bus:
        buses = BusService.search_buses(origin, dest, str(travel_date), sort_by=sort_by)
        st.subheader(f"Available Buses ({len(buses)})")
        if buses:
            for b in buses:
                with st.container(border=True):
                    bcol1, bcol2, bcol3, bcol4 = st.columns([3, 2, 2, 1.5])
                    with bcol1:
                        st.markdown(f"### {b['operator']}")
                        st.caption(f"Type: {b['bus_type']}")
                    with bcol2:
                        st.markdown(f"**Depart:** {b['departure']} ➔ **Arrive:** {b['arrival']}")
                        st.markdown(f"⏱️ Duration: `{b['duration_str']}`")
                    with bcol3:
                        st.markdown(f"Fare: **{format_currency(b['fare'])}**")
                        st.caption(f"Seats: {b['available_seats']} Left")
                    with bcol4:
                        if st.button("Book Bus", key=f"bk_bus_{b['id']}", type="primary", width="stretch"):
                            st.session_state["active_booking_item"] = {
                                "category": "Bus",
                                "provider": b["operator"],
                                "title": f"{b['operator']} - {b['bus_type']}",
                                "amount": b["fare"],
                                "date": str(travel_date)
                            }
                            st.rerun()

    # 3. FLIGHTS
    with t_tab_flight:
        flights = FlightService.search_flights(origin, dest, str(travel_date), sort_by=sort_by)
        st.subheader(f"Available Flights ({len(flights)})")
        if flights:
            for f in flights:
                with st.container(border=True):
                    fcol1, fcol2, fcol3, fcol4 = st.columns([3, 2, 2, 1.5])
                    with fcol1:
                        st.markdown(f"### {f['provider']}")
                        st.caption(f"Flight #{f['flight_number']}")
                    with fcol2:
                        st.markdown(f"**Depart:** {f['departure']} ➔ **Arrive:** {f['arrival']}")
                        st.markdown(f"⏱️ Duration: `{f['duration_str']}`")
                    with fcol3:
                        st.markdown(f"Economy: **{format_currency(f['price_economy'])}**")
                        st.caption(f"Seats: {f['seats_available']}")
                    with fcol4:
                        if st.button("Book Flight", key=f"bk_flt_{f['id']}", type="primary", width="stretch"):
                            st.session_state["active_booking_item"] = {
                                "category": "Flight",
                                "provider": f["provider"],
                                "title": f"{f['provider']} ({f['flight_number']})",
                                "amount": f["price_economy"],
                                "date": str(travel_date)
                            }
                            st.rerun()

    # 4. CABS
    with t_tab_cab:
        st.subheader("Dedicated Outstation Cabs")
        cab_types = [
            {"type": "Sedan (Dzire / Etios)", "capacity": "4 Passengers", "rate": 4500.0, "time": "8-10 hrs"},
            {"type": "SUV (Innova Crysta)", "capacity": "6-7 Passengers", "rate": 6800.0, "time": "8-10 hrs"},
            {"type": "Tempo Traveller", "capacity": "12 Passengers", "rate": 11500.0, "time": "9-11 hrs"}
        ]
        for c in cab_types:
            with st.container(border=True):
                ccol1, ccol2, ccol3, ccol4 = st.columns([3, 2, 2, 1.5])
                with ccol1:
                    st.markdown(f"### {c['type']}")
                    st.caption(f"Capacity: {c['capacity']}")
                with ccol2:
                    st.markdown(f"**Flexible Departure**")
                    st.markdown(f"Estimated Travel Time: `{c['time']}`")
                with ccol3:
                    st.markdown(f"Fare: **{format_currency(c['rate'])}**")
                    st.caption("Tolls & Fuel Included")
                with ccol4:
                    if st.button("Book Cab", key=f"bk_cab_{c['type']}", type="primary", width="stretch"):
                        st.session_state["active_booking_item"] = {
                            "category": "Cab",
                            "provider": "Verified Outstation Fleet",
                            "title": f"Outstation Cab - {c['type']}",
                            "amount": c["rate"],
                            "date": str(travel_date)
                        }
                        st.rerun()

    # --- IN-APP BOOKING MODAL DIALOG ---
    if "active_booking_item" in st.session_state and st.session_state["active_booking_item"]:
        item = st.session_state["active_booking_item"]
        with st.container(border=True):
            st.markdown(f"### 🎫 Complete In-App Booking: {item['category']}")
            st.markdown(f"**Selected:** {item['title']} | **Date:** {item['date']}")
            st.markdown(f"**Fare Payable:** **{format_currency(item['amount'])}** *(Demo Secure Transaction)*")
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                pass_name = st.text_input("Passenger / Guest Name", value=st.session_state.get("user_name", "Rohit Sharma"), key="trans_pass_name")
            with p_col2:
                pass_age = st.number_input("Passenger Age", min_value=1, max_value=110, value=29, key="trans_pass_age")

            pay_method = st.radio("Payment Gateway", ["UPI (Google Pay / PhonePe) - Demo", "Credit / Debit Card - Demo", "Net Banking - Demo"], horizontal=True)

            b_btn_col1, b_btn_col2 = st.columns(2)
            with b_btn_col1:
                if st.button("✅ Pay & Confirm Booking", type="primary", width="stretch"):
                    res = BookingService.book_ticket(
                        user_id=user_id,
                        category=item["category"],
                        provider_name=item["provider"],
                        item_title=item["title"],
                        travel_date=item["date"],
                        passenger_count=1,
                        total_amount=item["amount"],
                        passengers=[{"name": pass_name, "age": pass_age, "seat": "Confirmed"}],
                        payment_method=pay_method
                    )
                    st.success(f"🎉 Booking Confirmed! PNR/Reference: **`{res['booking_reference']}`**")
                    st.session_state["active_booking_item"] = None
                    st.balloons()
            with b_btn_col2:
                if st.button("Cancel", width="stretch"):
                    st.session_state["active_booking_item"] = None
                    st.rerun()


render_transportation_page()

